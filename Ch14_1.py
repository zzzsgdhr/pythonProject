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
# define default stock number
stock_num = 'sz000722'


def datetime_parser(bs):
  # get published datetime in HTML
  datetime = str(bs.find(string=lambda text: isinstance(text, Comment))).lstrip(' [ published at ').rstrip(' ] ')
  if not re.match('^\d{4}-\d{2}-\d{2}[\S\s]+$', datetime):
    datetime = '1991-01-01'  # default datetime

  return datetime


def html_saver(page, page_bs):
  # save html to local file
  with open('HTMLs/{}-{}.html'.format(stock_num, page.newstitle), 'wb') as f:
    f.write(page_bs.prettify().encode('utf-8'))


def main(stocknum=None):

  if stocknum is not None:
    stock_num = stocknum

  res = []
  ht = requests.get(
    'http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/{}.phtml'.format(stock_num),
    headers=headers
  ).content.decode('gb2312')
  stock_news_page = namedtuple('StockNewsPage', ['newstitle', 'newsurl'])

  try:
    page_list = [stock_news_page(newstitle=one.text, newsurl=one['href']) for one in
                 BeautifulSoup(ht, 'lxml').find('div', {'class': 'datelist'}).find('ul').findAll('a')]
  except AttributeError:
    print('this stock may not exist')
    return None
  # pprint(page_list)


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
     bs.findAll('div', {'id': 'sina-header'}) +
     bs.findAll('div', {'class': 'article-content-right'}) +
     bs.findAll('div', {'class': 'path-search'}) +
     bs.findAll('div', {'class': 'page-tools'}) +
     bs.findAll('div', {'class': 'page-right-bar'}) +
     bs.findAll('div', {'class': 'most-read'}) +
     bs.findAll('div', {'class': 'blk-wxfollow'}) +
     bs.findAll('div', {'class': 'blk-related'}) +
     bs.findAll('div', {'class': 'article-bottom-tg'}) +
     bs.findAll('div', {'class': 'article-bottom'}) +
     bs.findAll('link', {'href': '//finance.sina.com.cn/other/src/sinafinance.article.min.css'}) +
     bs.findAll('div', {'class': 'article-content-right'}) +
     bs.findAll('div', {'class': 'block-comment'}) +
     bs.findAll('div', {'class': 'sina-header'}) +
     bs.findAll('div', {'class': 'path-search'}) +
     bs.findAll('div', {'class': 'top-bar-wrap'}) +
     bs.findAll('div', {'class': 'blk-related'}) +
     bs.findAll('div', {'class': 'most-read'}) +
     bs.findAll('div', {'class': 'ad'}) +
     bs.findAll('div', {'class': 'new_style_article'}) +
     bs.findAll('div', {'class': 'feed-card-content'}) +
     bs.findAll('div', {'class': 'page-footer'}) +
     bs.findAll('div', {'class': 'sina15-top-bar-wrap'}) +
     bs.findAll('div', {'class': 'site-header clearfix'}) +
     bs.findAll('div', {'class': 'right'}) +
     bs.findAll('div', {'class': 'bottom-tool'}) +
     bs.findAll('div', {'class': 'most-read'}) +
     bs.findAll('div', {'id': 'lcs_wrap'}) +
     bs.findAll('div', {'class': 'lcs1_w'}) +
     bs.findAll('div', {'class': 'desktop-side-tool'}) +
     bs.findAll('div', {'class': 'feed-wrap'}) +
     bs.findAll('div', {'class': 'article-info clearfix'}) +
     bs.findAll('a', {'href': 'http://finance.sina.com.cn/focus/gmtspt.html'}) +
     bs.findAll('iframe', {'class': 'sina-iframe-content'})

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
      'stock': stock_num,
      'title': bs.find('h1').text,
      'html': str(bs).replace('\n', ''),
      'datetime': datetime_parser(bs)  # find datetime info in HTML comment

    }
    res.append(d_res)

  return res


if __name__ == '__main__':
  res = main('sz000722')
  pprint(res)
