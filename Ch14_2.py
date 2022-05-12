
import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import time
import logging
from pprint import pprint
import re
from bs4 import Comment

logging.basicConfig(level=logging.DEBUG)

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}
# define stock number
stock_id = 'BIDU'


def datetime_parser(bs):
  datetime = str(bs.find(string=lambda text: isinstance(text, Comment))).lstrip(' [ published at ').rstrip(' ] ')
  if not re.match('^\d{4}-\d{2}-\d{2}[\S\s]+$', datetime):
    datetime = '1991-01-01'  # default datetime

  return datetime


def html_saver(page, page_bs):
  with open('HTMLs/{}-{}.html'.format(stock_id, page.newstitle), 'wb') as f:
    f.write(page_bs.prettify().encode('utf-8'))


def main(stocknum=None):

  if stocknum is not None:
    stock_num = stocknum

  res = []
  ht = requests.get(
    'http://biz.finance.sina.com.cn/usstock/usstock_news.php?pageIndex=1&symbol={}&type=1'.format(stock_num),
    headers=headers
  ).content.decode('gb2312')
  stock_news_page = namedtuple('StockNewsPage', ['newstitle', 'newsurl'])

  try:
    page_list = [stock_news_page(newstitle=one.find('a').text, newsurl=one.find('a')['href']) for one in
                 BeautifulSoup(ht, 'lxml').findAll('ul', {'class': 'xb_list'})[-1].findAll('li')]
  except AttributeError as e:
    print('this stock may not exist')
    return None
  pprint(page_list)


  for page in page_list[:]:
    logging.debug('visiting next page')
    time.sleep(2)  # 2 seconds' waiting
    ht = requests.get(page.newsurl, headers=headers).content.decode('utf-8')
    bs = BeautifulSoup(ht, 'lxml')

    # remove all unnecessary tags
    [s.decompose() for s in
     bs('script') +
     bs('noscript') +
     bs('style') +
     bs.findAll('div', {'class': 'top-banner'}) +
     bs.findAll('div', {'class': 'hqimg_related'}) +
     # 更多的页面元素清洗
     # ......
     bs.findAll('div',{'class':'new_style_article'})
     ]

    # try to make article-content div in the middle of page
    try:
      bs.find('div', {'class': 'article-content-left'})['class'] = 'article-content'
    except Exception as e:
      bs.find('div', {'class': 'left'})['class'] = 'article-content'
    finally:
      pass

    html_saver(page, bs)
    for one in bs.findAll('a', {'class': 'keyword'}):
      one.attrs = {}  # remove clickable href

    d_res = {
      'stock': 'us-'+stock_num,
      'title': bs.find('h1').text,
      'html': str(bs).replace('\n', ''),
      'datetime': datetime_parser(bs)  # find datetime info in HTML comment

    }
    res.append(d_res)

  return res


if __name__ == '__main__':
  res = main('BIDU')
  pprint(res)
