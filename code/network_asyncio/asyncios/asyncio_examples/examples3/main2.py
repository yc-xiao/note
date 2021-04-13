import asyncio
import aiohttp
import hashlib
import time
import os

auth = aiohttp.BasicAuth(login='youcan', password='youcan')

file_path = 'tt.tar'
file_type = 'pipeline'
chunk_num = 1000
step = chunk_num//10

async def upload_chunk(s, index, chunck_index_dic, error_index, sem):
    async with sem:
        file_data, md5 = read_file(index)
        url = 'http://127.0.0.1:8000/api/analysis_modules/1/file_upload2/'
        data = {'filename': file_path, 'file_type': file_type,
            'chunk_file': file_data, 'chunk_md5': md5, 'chunk_index': str(index)}
        if index in chunck_index_dic and chunck_index_dic[index] == md5:
            return

        async with s.post(url, data=data, auth=auth) as response:
            result = await response.json()
            print(result)
            if response.status != 200:
                error_index.append(index)

def read_file(i):
    size = os.path.getsize(file_path)
    index = size//chunk_num
    with open(file_path, 'rb') as f:
        f.seek(index*i)
        file_data = f.read(index) if i+1 != chunk_num else f.read()
        s_hashlib = hashlib.md5()
        s_hashlib.update(file_data)
        md5 = s_hashlib.hexdigest()
    return file_data, md5

async def check_chuck(check_index):
    error_index = []
    sem = asyncio.Semaphore(20)
    async with aiohttp.ClientSession() as s:
        url = 'http://127.0.0.1:8000/api/analysis_modules/1/file_upload1/'
        data = {'filename': file_path, 'file_type': file_type, 'indexs': check_index}
        async with s.post(url, json=data, auth=auth) as response:
            chunck_index = await response.json()
            chunck_index_dic = {_['index']: _['md5'] for _ in chunck_index['results']}

        tasks = [upload_chunk(s, index, chunck_index_dic, error_index, sem) for index in check_index]
        await asyncio.gather(*tasks)

    return error_index

async def check_chuck_ok(check_index):
    error_index = []
    async with aiohttp.ClientSession() as s:
        url = 'http://127.0.0.1:8000/api/analysis_modules/1/file_upload1/'
        data = {'filename': file_path, 'file_type': file_type, 'indexs': check_index}
        async with s.post(url, json=data, auth=auth) as response:
            chunck_index = await response.json()
            chunck_index_dic = {_['index']: _['md5'] for _ in chunck_index['results']}

        url = 'http://127.0.0.1:8000/api/analysis_modules/1/file_upload2/'
        for index in check_index:
            file_data, md5 = read_file(index)
            data = {'filename': file_path, 'file_type': file_type,
                'chunk_file': file_data, 'chunk_md5': md5, 'chunk_index': str(index)}
            if index in chunck_index_dic and chunck_index_dic[index] == md5:
                continue

            async with s.post(url, data=data, auth=auth) as response:
                result = await response.json()
                print(result)
                if response.status != 200:
                    error_index.append(index)
    return error_index

async def send():
    url = 'http://127.0.0.1:8000/api/analysis_modules/1/file_upload3/'
    data = {'filename': file_path, 'file_type': file_type}
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=data, auth=auth) as response:
            result = await response.json()
            print(result)

async def main():
    chunk_index = [i for i in range(chunk_num)]
    # 所有块都上传成功
    while len(chunk_index) != 0:
        # 取出step块进行上传
        temp_index = []
        for i in range(step):
            if len(chunk_index):
                temp_index.append(chunk_index.pop())

        # error_index 上传未成功
        error_index = await check_chuck(temp_index)
        for index in error_index:
            chunk_index.append(index)

    # 发送合并通知
    # await send()


if __name__ == '__main__':
    s1 = time.time()
    asyncio.run(main())
    print(time.time() - s1)
