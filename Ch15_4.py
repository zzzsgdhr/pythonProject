from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
  crawl_config = {
  }

  @every(minutes=24 * 60)
  def on_start(self):
    self.crawl('https://bbs.hupu.com/xuefu', fetch_type='js', callback=self.index_page)

  @config(age=10 * 24 * 60 * 60)
  def index_page(self, response):
    for each in response.doc('a[href^=http]').items():
      url = each.attr.href
      if re.match(r'^http\S*://bbs.hupu.com/\d+.html$', url):
        self.crawl(url, fetch_type='js', callback=self.detail_page)

    next_page_url = response.doc(
      '#container > div > div.bbsHotPit > div.showpage > div.page.downpage > div > a.nextPage').attr.href

    if int(next_page_url[-1]) > 30:
      raise ValueError

    self.crawl(next_page_url,
               fetch_type='js',
               callback=self.index_page)

  @config(priority=2)
  def detail_page(self, response):
    return {
      "url": response.url,
      "title": response.doc('#j_data').text(),
    }
