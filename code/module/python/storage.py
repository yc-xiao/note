
from botocore.exceptions import ClientError
from botocore.client import Config
from qcloud_cos.cos_exception import CosClientError, CosServiceError
from qcloud_cos import CosS3Client
from qcloud_cos import CosConfig
from tempfile import NamedTemporaryFile
from urllib import parse
from .time import duration, get_now
from .logger import logger
import mimetypes
import boto3

def get_mimetype(filename):
    return mimetypes.guess_type(filename)[0]

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

class S3Helper:
    def __init__(self, bucket='', region_name='', aws_access_key_id='', aws_secret_access_key='', **kwargs) -> None:
        self.bucket = bucket
        kwargs['region_name'] = region_name
        kwargs['aws_access_key_id'] = aws_access_key_id
        kwargs['aws_secret_access_key'] = aws_secret_access_key
        self.s3_client = boto3.client('s3', **kwargs)

    def exists(self, key, bucket=None):
        bucket = bucket or self.bucket
        try:
            if key[-1] != '/':
                self.s3_client.head_object(Bucket=bucket, Key=key)
                return True
            else:
                return key in self.list_objects(key, remove=False)['prefixs']
        except ClientError as e:
            logger.warning(e)
        return False

    def list_objects(self, prefix, delimiter='/', remove=True, bucket=None):
        """
            delimiter: ['', '/']，推荐delimiter='/'。
                当delimiter='/'，仅查询prefix第一层子集，response包含CommonPrefixes字段。
                当delimiter=''，response不包含CommonPrefixes字段，Contents包含prefix所有的对象。
        """
        bucket = bucket or self.bucket
        data, count, marker = {'keys': set(), 'prefixs': set()}, 0, ''
        # 当delimiter存在时，prefix必须有后缀'/'
        if delimiter == '/' and (not prefix or prefix[-1] != '/'):
            prefix += '/'
        kw = {'Bucket':bucket, 'Prefix': prefix, 'Delimiter': delimiter}
        while count < 1000:
            response = self.s3_client.list_objects_v2(**kw)
            keys = set()
            for each in response.get('CommonPrefixes', []):
                keys.add(each['Prefix'])
            for each in response.get('Contents', []):
                keys.add(each['Key'])
            for key in keys:
                k = 'prefixs' if key[-1] == '/' else 'keys'
                data[k].add(key)
            marker = response.get('NextContinuationToken', None)
            if not marker:
                break
            kw['ContinuationToken'] = marker
            count += 1
        if remove:
            if prefix in data['prefixs']:
                data['prefixs'].remove(prefix)
            if prefix in data['keys']:
                data['keys'].remove(prefix)
        return data

    @duration()
    def upload(self, prefix, local_file='', url=False, bucket=None, extra_params={}, expires_in=300, download_expires_in=0):
        bucket = bucket or self.bucket
        if url:
            params = {'Bucket': bucket, 'Key': prefix}
            params.update(extra_params)
            # https://stackoverflow.com/questions/66657107/aws-s3-go-sdk-presigned-url-unable-upload-file-when-add-acl/74585074#74585074
            # 预签名设置ACL存在问题，单独的put_object支持ACL。
            # fix: 可通过预签名上传，后再更新object的acl。或直接通过put_object上传对象并设置acl。
            return self.s3_client.generate_presigned_url('put_object', Params=params, ExpiresIn=expires_in)
        upload_flag = False
        for _ in range(3):
            try:
                mime_type = get_mimetype(prefix)
                if mime_type:
                    extra_params['ContentType'] = mime_type
                self.s3_client.upload_file(local_file, bucket, prefix, ExtraArgs=extra_params)
                upload_flag = True
                break
            except ClientError as e:
                logger.warning(e)
        # 本地文件上传后，可以通过download_expires_in获取文件下载链接
        if upload_flag and download_expires_in:
            return self.download(prefix=prefix, url=True, bucket=bucket, expires_in=download_expires_in)
        return upload_flag

    @duration()
    def download(self, prefix, url=False, bucket=None, filename='', extra_params={}, expires_in=300):
        '''
            文件下载
            参数说明：
                bucket和prefix指定文件路径
                url = true，开启预链接下载，可设置filename，expires_in，extra_params参数。返回值为 url 或 None
                url = false，开启本地下载，默认下载到临时文件。可设置filename设置下载路径。返回值为 临时文件对象 或 filename 或 None
        '''
        bucket = bucket or self. bucket
        if url:
            params = {'Bucket': bucket, 'Key': prefix}
            mime_type = get_mimetype(prefix)
            if mime_type:
                params['ResponseContentType'] = mime_type
            # ResponseContentDisposition 访问文件时，使用下载或浏览器访问
            # {'ResponseContentDisposition': 'attachment;filename={filename}'}， 可设置下载文件名称
            filename = filename or prefix.split('/')[-1] # 可指定下载文件名称
            if filename.split('.')[-1] in ['img', 'jpg', 'jpeg', 'png', 'pdf']:
                params['ResponseContentDisposition'] = parse.quote('inline')
            else:
                params['ResponseContentDisposition'] = parse.quote(f'attachment;filename="{filename}"')
            params.update(extra_params)
            return self.s3_client.generate_presigned_url('get_object', Params=params, ExpiresIn=expires_in)
        temp_file = None
        if not filename:
            temp_file = NamedTemporaryFile()
            filename = temp_file.name
        for _ in range(0, 3):
            try:
                self.s3_client.download_file(bucket, prefix, filename)
                return temp_file or filename
            except ClientError as e:
                logger.warning(f'cos_download_file err -> {e}')

    @duration()
    def multipart_upload(self, key, number=100, expires_in=3*3600, bucket=None):
        # 分片上传流程： https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/mpuoverview.html#mpu-process
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/create_multipart_upload.html#
        # 上传链接存在有效期。分片文件不存在有效期，需要手动确认完全上传与停止。
        bucket = bucket or self.bucket
        response = self.s3_client.create_multipart_upload(Bucket=bucket, Key=key)
        upload_id = response['UploadId']
        return self.list_parts(key, upload_id, number, expires_in, bucket)

    def list_parts(self, key, upload_id, number=100, expires_in=3*3600, bucket=None):
        try:
            bucket = bucket or self.bucket
            results = {'upload_id': upload_id, 'urls': [], 'parts': []}
            resp = self.s3_client.list_parts(Bucket=bucket, Key=key, MaxParts=number,UploadId=upload_id)
            uploaded_number = set()
            for each in resp.get('Parts', []):
                each['ETag'] = each['ETag'].replace('"', '')
                if each['Size'] >= 5*1024*1024:
                    uploaded_number.add(each['PartNumber'])
                results['parts'].append(each)
            for num in range(1, number+1):
                if num in uploaded_number:
                    continue
                url = self.s3_client.generate_presigned_url('upload_part', ExpiresIn=expires_in,
                                                            Params={'Bucket': bucket, 'Key': key, 'UploadId': upload_id, 'PartNumber': num})
                results['urls'].append({'url': url, 'PartNumber': num})
            return results
        except Exception as e:
            logger.warning(e)
            error_message = str(e)
            assert False, error_message

    def complete_multipart_upload(self, key, upload_id, number, bucket=None):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/complete_multipart_upload.html
        # parts [{"ETag": "5f363e0e58a95f06cbe9bbc662c5dfb6", "PartNumber": 2}]
        bucket = bucket or self.bucket
        try:
            results = self.list_parts(key, upload_id, number=number)
            # 根据parts进行合并，假设分片100块，只上传第2块。则parts = [{'PartNumber':2, 'ETag':'md5'}]，可以合并，但文件为第2块分片。
            parts = [{'PartNumber': part['PartNumber'], 'ETag': part['ETag']} for part in results['parts']]
            self.s3_client.complete_multipart_upload(Bucket=bucket, Key=key, UploadId=upload_id, MultipartUpload={'Parts': parts})
        except Exception as e:
            logger.warning(e)
            error_message = str(e)
            if 'EntityTooSmall' in error_message:
                error_message = '分片上传文件，除最后一块，每块大小最少为5MB，请重新上传文件。。'
            elif 'MalformedXML' in error_message:
                error_message = '未找到上传的分片数据，请重新上传文件。'
            elif 'NoSuchUpload' in error_message:
                error_message = '上传id无效，请重新上传文件。'
            assert False, error_message

    def clear_multipart_upload(self, bucket=None):
        '''
            云端不会自动已上传的分块，需要手动清空。
            定时清空未使用的分块上传。
        '''
        bucket = bucket or self.bucket
        resp = self.s3_client.list_multipart_uploads(Bucket=bucket)
        expire = 3 * 24 * 60 * 60
        for upload in resp['Uploads']:
            total_seconds = (get_now() - upload['Initiated']).total_seconds()
            if total_seconds >= expire:
                self.s3_client.abort_multipart_upload(Bucket=bucket, Key=upload['Key'], UploadId=upload['UploadId'])

    def copy(self, source_key, dest_key, source_bucket=None, dest_bucket=None):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/copy.html
        # 复制如果存在值会覆盖掉
        source_bucket = source_bucket or self.bucket
        dest_bucket = dest_bucket or self.bucket
        source = {'Bucket': source_bucket, 'Key': source_key}
        if self.exists(dest_key, dest_bucket):
            logger.error(f'cp {source_bucket}/{source_key} {dest_bucket}{dest_key} 失败，文件已存在。')
            return False
        try:
            assert self.exists(dest_key, dest_bucket), '目标文件已存在。'
            self.s3_client.copy(source, dest_bucket, dest_key)
            return True
        except Exception as e:
            info = f'cp {source_bucket}/{source_key} {dest_bucket}{dest_key} 失败，{e}'
            logger.error(info)
        return False

    def get_public_file_url(self, key, bucket=None, filename=''):
        bucket = bucket or self.bucket
        assert self.exists(key, bucket), '文件不存在。'
        self.s3_client.put_object_acl(Key=key, Bucket=bucket, ACL='public-read')
        url = self.download(key, url=True, bucket=bucket, filename=filename)
        return url.split('?')[0]


# https://cloud.tencent.com/document/product/436/12269
# cos兼容boto3，CosHelper 继承 S3Helper。可重写任意方法，通过self.cos_client调用。其余继承方法则由self.s3_helper.s3_client实现调用。
class CosHelper(S3Helper):
    def __init__(self, secret_id='', secret_key='', region='', bucket='') -> None:
        self.bucket = bucket
        self.config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
        self.cos_client = CosS3Client(self.config)

        # https://www.tencentcloud.com/zh/document/product/436/32537#python
        extra = {'endpoint_url': f'https://cos.{region}.myqcloud.com', 'config': Config(signature_version='s3', s3={'addressing_style': 'virtual'})}
        self.s3_helper = S3Helper(bucket, region, secret_id, secret_key, **extra)
        self.s3_client = self.s3_helper.s3_client

    def exists(self, key, bucket=None):
        bucket = bucket or self.bucket
        return self.cos_client.object_exists(bucket, key)

    @duration()
    def upload(self, prefix, local_file='', url=False, bucket=None, expires_in=300, download_expires_in=0):
        bucket = bucket or self.bucket
        if url:
            return self.cos_client.get_presigned_url(Method='PUT', Bucket=bucket, Key=prefix, Expired=expires_in)
        upload_flag = False
        for _ in range(3):
            try:
                # upload_file会自动设置Content-Type
                self.cos_client.upload_file(Bucket=bucket, Key=prefix, LocalFilePath=local_file, PartSize=20, MAXThread=3)
                upload_flag = True
                break
            except CosClientError or CosServiceError as e:
                logger.warning(f'cos_upload_file err -> {e}')
        # 本地文件上传后可以通过download_expires_in获取预签名下载链接
        if upload_flag and download_expires_in:
            self.download(prefix=prefix, url=True, bucket=bucket, expires_in=download_expires_in)
        return upload_flag


cos_helper = CosHelper()
s3_helper = S3Helper()