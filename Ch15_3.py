from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
  crawl_config = {
  }

  @every(minutes=24 * 60)
  def on_start(self):
    self.crawl('https://book.douban.com/', callback=self.index_page)

  @config(age=10 * 24 * 60 * 60)
  def index_page(self, response):
    for each in response.doc('a[href^="http"]').items():
      if re.match("https://book.douban.com/subject/\d+/\S+", each.attr.href, re.U):
        self.crawl(each.attr.href, callback=self.detail_page)

  @config(priority=2)
  def detail_page(self, response):
    review_url = response.doc(
      '#content > div > div.article > div.related_info > div.mod-hd > h2 > span.pl > a').attr.href
    return {
      "url": response.url,
      "title": response.doc('title').text(),
      "author": response.doc('#info > span:nth-child(1) > a').text(),
      "rating": response.doc('#interest_sectl > div > div.rating_self.clearfix > strong').text(),
      "reviews": review_url,
    }
