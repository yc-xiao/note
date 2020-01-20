# 例3
import types

@types.coroutine      # 将一个生成器变成一个awaitable的对象
def downloader():
    yield 'aaa'


async def download_url():   # 协程
    waitable = downloader()
    print(waitable)   # <generator object downloader at 0x1091e2c78>     生成器
    html = await waitable
    return html

def func():
    coro = download_url()
    print(coro)                # <coroutine object download_url at 0x1091c9d48>
    ret = coro.send(None)
    print(ret)

if __name__ == '__main__':
    func()
