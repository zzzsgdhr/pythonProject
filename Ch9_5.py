import aiohttp
import asyncio
# 使用aiohttp访问网页的例子
async def fetch(session, url):
  # 类似 requests.get
  async with session.get(url) as response:
    return await response.text()

# 通过async实现单线程并发IO
async def main():
  # 类似requests中的Session对象
  async with aiohttp.ClientSession() as session:
    html = await fetch(session, 'http://httpbin.org/headers')
    print(html)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
