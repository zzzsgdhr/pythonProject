from gain import Css, Item, XPathParser, Spider


class Post(Item):
  title = Css('#j_data')

  async def save(self):
    print(self.title)


class MySpider(Spider):
  start_url = 'https://bbs.hupu.com/xuefu'
  concurrency = 5
  headers = {'User-Agent': 'Google Spider'}
  parsers = [
    XPathParser('//*[@id="ajaxtable"]/div[1]/ul/li[*]/div[1]/a/@href', Post)
  ]

MySpider.run()
