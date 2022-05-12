import requests, json, time, logging, random, csv, lxml.html, jieba.analyse
from pprint import pprint
from datetime import datetime


# 京东评论 JS
class JDComment():
  _itemurl = ''

  def __init__(self, url, page):
    self._itemurl = url
    self._checkdate = None
    logging.basicConfig(
      # filename='app.log',
      level=logging.INFO,
    )
    self.content_sentences = ''
    self.max_page = page

  def go_on_check(self, date, page):
    go_on = self.date_check(date) and page <= self.max_page
    return go_on

  def set_checkdate(self, date):
    self._checkdate = datetime.strptime(date, '%Y-%m-%d')

  def get_comment_from_item_url(self):

    comment_json_url = 'https://sclub.jd.com/comment/productPageComments.action'
    p_data = {
      'callback': 'fetchJSON_comment98vv242411',
      'score': 0,
      'sortType': 3,
      'page': 0,
      'pageSize': 10,
      'isShadowSku': 0,
    }

    p_data['productId'] = self.item_id_extracter_from_url(self._itemurl)

    ses = requests.session()

    go_on = True
    while go_on:
      response = ses.get(comment_json_url, params=p_data)
      logging.info('-' * 10 + 'Next page!' + '-' * 10)
      if response.ok:

        r_text = response.text
        r_text = r_text[r_text.find('({') + 1:]
        r_text = r_text[:r_text.find(');')]
        js1 = json.loads(r_text)

        for comment in js1['comments']:
          go_on = self.go_on_check(comment['referenceTime'], p_data['page'])
          logging.info('{}\t{}\t{}\t{}'.format(comment['content'], comment['referenceTime'],
                                               comment['nickname'], comment['userClientShow']))

          self.content_process(comment)
          self.content_sentences += comment['content']

      else:
        logging.error('Status NOT OK')
        break

      p_data['page'] += 1
      self.random_sleep()  # delay

  def item_id_extracter_from_url(self, url):
    item_id = 0

    prefix = 'item.jd.com/'
    index = str(url).find(prefix)
    if index != -1:
      item_id = url[index + len(prefix): url.find('.html')]

    if item_id != 0:
      return item_id

  def date_check(self, date_here):
    if self._checkdate is None:
      logging.warning('You have not set the checkdate')
      return True
    else:
      dt_tocheck = datetime.strptime(date_here, '%Y-%m-%d %H:%M:%S')
      if dt_tocheck > self._checkdate:
        return True
      else:
        logging.error('Date overflow')
        return False

  def content_process(self, comment):
    with open('jd-comments-res.csv', 'a') as csvfile:
      writer = csv.writer(csvfile, delimiter=',')
      writer.writerow([comment['content'], comment['referenceTime'],
                       comment['nickname'], comment['userClientShow']])

  def random_sleep(self, gap=1.0):
    # gap = 1.0
    bias = random.randint(-20, 20)
    gap += float(bias) / 100
    time.sleep(gap)

  def get_keywords(self):
    content = self.content_sentences
    kws = jieba.analyse.extract_tags(content, topK=20)
    return kws


if __name__ == '__main__':

  url = input("输入商品链接：")
  date_str = input("输入限定日期：")
  page_num = int(input("输入最大爬取页数："))
  jd1 = JDComment(url, page_num)
  jd1.set_checkdate(date_str)
  print(jd1.get_comment_from_item_url())
  print(jd1.get_keywords())
