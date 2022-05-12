class JDComment():
  _itemurl = ''

  def __init__(self, url):
    self._itemurl = url
    logging.basicConfig(
      level=logging.INFO,
    )
    self.content_sentences = ''

  def get_comment_from_item_url(self):

    comment_json_url = 'https://sclub.jd.com/comment/productPageComments.action'
    p_data = {
      'callback': 'fetchJSON_comment98vv110378',
      'score': 0,
      'sortType': 3,
      'page': 0,
      'pageSize': 10,
      'isShadowSku': 0,
    }

    p_data['productId'] = self.item_id_extracter_from_url(self._itemurl)

    ses = requests.session()

    while True:
      response = ses.get(comment_json_url, params=p_data)
      logging.info('-' * 10 + 'Next page!' + '-' * 10)
      if response.ok:
        r_text = response.text
        r_text = r_text[r_text.find('({'} + 1:)
        r_text = r_text[:r_text.find(');'])
        js1 = json.loads(r_text)

        for comment in js1['comments']:
          logging.info('{}\t{}\t{}\t{}'.format(comment['content'], comment['referenceTime'],
                                               comment['nickname'], comment['userClientShow']))

          self.content_process(comment)
          self.content_sentences+=comment['content']
      else:
        logging.error('Status NOT OK')
        break

      p_data['page'] += 1
      if p_data['page'] > 50:
        logging.warning('We have reached at 50th page')
        break

  def item_id_extracter_from_url(self, url):
    item_id = 0

    prefix = 'item.jd.com/'
    index = str(url).find(prefix)
    if index != -1:
      item_id = url[index + len(prefix): url.find('.html')]

    if item_id != 0:
      return item_id

  def content_process(self, comment):
    with open('jd-comments-res.csv','a') as csvfile:
      writer = csv.writer(csvfile,delimiter=',')
      writer.writerow([comment['content'],comment['referenceTime'],
                       comment['nickname'],comment['userClientShow']])
