import requests
import time
from pymongo import MongoClient

# client = MongoClient('mongodb://yourserver:yourport/')
client = MongoClient() # 使用Pymongo对数据库进行初始化，由于我们使用了本地mongodb，因此此处不需要配置，
# 等效于client = MongoClient('localhost', 27017)

# 使用名为"ctrip"的数据库
db = client['ctrip']
# 使用其中的collection表：hotelfaq（酒店常见问答）
collection = db['hotelfaq']
global hotel
global max_page_num
# 原始数据获取URL
raw_url = 'http://hotels.ctrip.com/Domestic/tool/AjaxHotelFaqLoad.aspx?'
# 根据开发者工具中的request header信息来设置headers
headers = {
  'Host': 'hotels.ctrip.com',
  'Referer': 'http://hotels.ctrip.com/hotel/473871.html',
  'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
}
# 我们在此只使用了Host、Referer、UA这几个关键字段

def get_json(hotel, page):
  params = {
    'hotelid': hotel,
    'page': page
  }
  try:
    # 使用request中get方法的params参数
    res = requests.get(raw_url, headers=headers, params=params)
    if res.ok: # 成功访问
      return res.json() # 返回json
  except Exception as e:
    print('Error here:\t', e)

# JSON数据处理
def json_parser(json):
  if json is not None:
    asks_list = json.get('AskList')
    if not asks_list:
      return None
    for ask_item in asks_list:
      one_ask = {}
      one_ask['id'] = ask_item.get('AskId')
      one_ask['hotel'] = hotel
      one_ask['createtime'] = ask_item.get('CreateTime')
      one_ask['ask'] = ask_item.get('AskContentTitle')
      one_ask['reply'] = []
      if ask_item.get('ReplyList'):
        for reply_item in ask_item.get('ReplyList'):
          one_ask['reply'].append((reply_item.get('ReplierText'),
                                   reply_item.get('ReplyContentTitle'),
                                   reply_item.get('ReplyTime')
                                   ))
        yield one_ask # 使用生成器yield方法

# 存储到数据库
def save_to_mongo(data):
  if collection.insert(data): # 插入一条数据
    print('Saving to db!')

# 工作函数
def worker(hotel):
  max_page_num = int(input('input max page num:')) # 输入最大页数（通过观察问答网页可以得到）
  for page in range(1, max_page_num + 1):
    time.sleep(1.5) # 访问间隔，避免服务器由于过高压力而拒绝访问
    print('page now:\t{}'.format(page))
    raw_json = get_json(hotel, page) # 获取原始JSON数据
    res_set = json_parser(raw_json)
    for res in res_set:
      print(res)
      save_to_mongo(res)


if __name__ == '__main__':
  hotel = int(input('input hotel id:'))  # 以本例而言，hotelid为473871
  worker(hotel)
