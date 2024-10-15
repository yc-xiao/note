import pandas as pd
import numpy as np
import tempfile
import tarfile
import zipfile
import copy
import os

def upload_excel(file, read_excel={}, required='*'):
    # https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
    df = pd.read_excel(file, comment='##', **read_excel) # 若单元格中有##，则忽略该单元格与单元格后的"整行"
    df = df.dropna(how='all') # 删除整行为空的行
    df = df.replace({np.nan:None}) # 将nan替换为None
    if required:
        column_map = {}
        for c in df.columns:
            if required in c:
                assert not df[c].isnull().any(), f'{c}是必填项。'
                column_map[c] = c[1:]
        df.rename(columns=column_map, inplace=True)
    data = df.to_dict(orient='records')
    return data

def combine(data:any) -> list:
    """
        data = [{'a':1, 'b': [1,2], 'c': {'c1':1}}]
        new_data = [{'a':1, 'b':1, 'c1':1}, {'a':1, 'b':2, 'c1':1}]
    """
    new_data = []
    if isinstance(data, (list, tuple, set)):
        for d in data:
            new_data.extend(combine(d))
    elif isinstance(data, dict):
        new_data.append({})
        for k, v in data.items():
            _new_data = []
            for each in new_data:
                for value in combine(v):
                    _each = copy.copy(each) # copy.deepcopy
                    if isinstance(value, dict):
                        _each.update(value)
                    else:
                        _each[k] = value
                    _new_data.append(_each)
            new_data = _new_data
    else:
        new_data.append(data)
    return new_data

def test_pack_files(pack_type='zip'):
    temp_dir = tempfile.TemporaryDirectory()
    files = []
    for i in range(10):
        filepath = os.path.join(temp_dir.name, f'{i}.txt')
        with open(filepath, 'w') as f:
            f.writelines([filepath for j in range(10)])
        files.append({'filename': '', 'filepath': filepath})
    # 如果需要固定文件名称，可以先创建temp_dir，再目录下指定文件名称。
    # 临时目录和临时文件，默认情况下会自动回收。
    temp_file = tempfile.NamedTemporaryFile(suffix=f'.{pack_type}')
    pack_files(temp_file.name, files, pack_type=pack_type)
    return temp_dir, temp_file

def pack_files(pack_file, files, pack_type='zip', extra_params={}):
    '''
        pack_file 打包文件路径 如: /tmp/pack.zip
        files  打包文件集合 如: [{'filepath': '/tmp/tmp_dir/aa.pdf', 'filename': 'aa.pdf'}]
        pack_type 打包类型 如: zip
        extra_params 如: zip或tar包加密等
    '''
    for file in files:
        file['filename'] = file['filename'] or os.path.split(file['filepath'])[-1]
    if pack_type == 'zip':
        with zipfile.ZipFile(pack_file, 'w') as zf:
            for file in files:
                zf.write(file['filepath'], arcname=file['filename'])
    elif pack_type in ['tar', 'tar.gz']:
        mode = 'w' if pack_type == 'tar' else 'w:gz'
        with tarfile.open(pack_file, mode) as tf:
            for file in files:
                tf.add(name=file['filepath'], arcname=file['filename'])
