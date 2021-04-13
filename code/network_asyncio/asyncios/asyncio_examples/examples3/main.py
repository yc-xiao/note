# 异步请求
import aiohttp
import asyncio
import hashlib
import pdb
import os

auth = aiohttp.BasicAuth(login='youcan', password='youcan')

file_path = 'tt.tar'
file_type = 'database'
chunk_num = 1000

def check_md5_sum(file_name, hash_factory=hashlib.md5, chunk_num_blocks=1024*100):
    h = hash_factory()

    with open(file_name, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_num_blocks*h.block_size), b''):
            h.update(chunk)
    return h.hexdigest()

import time
t1 = time.time()
complete_file_md5 = check_md5_sum(file_path)
# complete_file_md5 = '28d1cd4cf51b07b3ce53ed4ce682095f'
print(complete_file_md5)
t2 = time.time()
print(t2-t1)

def read_all_file():
    size = os.path.getsize(file_path)
    index = size//chunk_num
    with open(file_path, 'rb') as f:
        datas = []
        for i in range(chunk_num):
            file_data = f.read(index) if chunk_num != i+1 else f.read()
            s_hashlib = hashlib.md5()
            s_hashlib.update(file_data)
            md5 = s_hashlib.hexdigest()
            datas.append({'md5': md5, 'index': i})
    return datas

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

async def search(s):
    # 查询
    url = 'http://127.0.0.1:8000/api/analysis_modules/1/file_part_pre_upload/'
    chunks = read_all_file()
    data = {'chunks': chunks, 'file_type': file_type, 'complete_file_name': file_path}
    response = await s.post(url, json=data, auth=auth)
    result = await response.json()
    print(result)
    return result

async def upload(s, chunk, sem):
    async with sem:
        # 异步上传
        url = 'http://127.0.0.1:8000/api/analysis_modules/1/file_part_upload/'
        index = chunk['index']
        chunk_file, md5 = read_file(index)
        data = {
            'file_type': file_type,
            'complete_file_name': file_path,
            'chunk_index': str(index),
            'chunk_file': chunk_file,
            'chunk_md5': md5,
            'complete_file_md5': complete_file_md5
        }
        response = await s.post(url, data=data, auth=auth)
        result = await response.json()
        return result

async def upload2(chunk, sem):
    async with sem:
        async with aiohttp.ClientSession() as s:
            # 异步上传
            url = 'http://127.0.0.1:8000/api/analysis_modules/1/file_part_upload/'
            index = chunk['index']
            chunk_file, md5 = read_file(index)
            data = {
                'file_type': file_type,
                'complete_file_name': file_path,
                'chunk_index': str(index),
                'chunk_file': chunk_file,
                'chunk_md5': md5,
                'complete_file_md5': complete_file_md5
            }
            response = await s.post(url, data=data, auth=auth)
            result = await response.json()
            return result

def callback(task):
    print(task.result())

async def main():
    async with aiohttp.ClientSession() as session:
        ss1 = time.time()
        result = await search(session)
        ss2 = time.time()
        print(ss2-ss1)
        tasks = []
        sem = asyncio.Semaphore(20)
        for chunk in result['results']['chunks']:
            if not chunk['is_upload']:
                task = asyncio.create_task(upload(session, chunk, sem))
                # task.add_done_callback(callback)
                tasks.append(task)
        await asyncio.gather(*tasks)
        await session.close()

async def main2():
    async with aiohttp.ClientSession() as session:
        result = await search(session)

    tasks = []
    sem = asyncio.Semaphore(500)
    for chunk in result['results']['chunks']:
        if not chunk['is_upload']:
            task = asyncio.create_task(upload2(chunk, sem))
            task.add_done_callback(callback)
            tasks.append(task)
    await asyncio.gather(*tasks)
    await session.close()

asyncio.run(main())
t3 = time.time()
print(t3-t2)
