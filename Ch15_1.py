from gain import Css, Item, Parser, Spider
import aiofiles


class Post(Item):
  title = Css('#hs_cos_wrapper_name')
  content = Css('.post-body')

  async def save(self):
    async with aiofiles.open('scrapinghub.txt', 'a+') as f:
      await f.write('{}\n'.format(self.results['title']))


class MySpider(Spider):
  concurrency = 5
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
  start_url = 'https://blog.scrapinghub.com/'
  parsers = [Parser('https://blog.scrapinghub.com/page/\d+/'),
             Parser('https://blog.scrapinghub.com/\d{4}/\d{2}/\d{2}/[a-z0-9\-]+', Post)]

MySpider.run()
