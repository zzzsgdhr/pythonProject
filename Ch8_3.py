import requests, time
from lxml import html

class NewsmthCrawl():
  header_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                 'Accept-Encoding': 'gzip, deflate, sdch, br',
                 'Accept-Language': 'zh-CN,zh;q=0.8',
                 'Connection': 'keep-alive',
                 'Upgrade-Insecure-Requests': '1',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                 }

  def set_startpage(self, startpagenum):
    self.start_pagenum = startpagenum

  def set_maxpage(self, maxpagenum):
    self.max_pagenum = maxpagenum

  def set_kws(self, kw_list):
    self.kws = kw_list

  def keywords_check(self, kws, str):
    if len(kws) == 0 or len(str) == 0:
      return False
    else:
      if any(kw in str for kw in kws):
        return True
      else:
        return False

  def get_all_items(self):
    res_list = []
    ses = requests.Session()

    raw_urls = ['http://www.newsmth.net/nForum/board/Joke?ajax&p={}'.
                  format(i) for i in range(self.start_pagenum, self.max_pagenum)]
    for url in raw_urls:
      resp = ses.get(url, headers=NewsmthCrawl.header_data)
      h1 = html.fromstring(resp.content)
      raw_xpath = '//*[@id="body"]/div[3]/table/tbody/tr'

      for one in h1.xpath(raw_xpath):
        tup = (one.xpath('./td[2]/a/text()')[0], 'http://www.newsmth.net' + one.xpath('./td[2]/a/@href')[0],
               one.xpath('./td[8]/a/text()')[0])
        res_list.append(tup)

      time.sleep(1.2)

    return res_list
