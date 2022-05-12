import requests
import json
from pprint import pprint

urls = ['http://hotels.ctrip.com/Domestic/tool/AjaxHotelFaqLoad.aspx?hotelid=473871&currentPage={}'.format(i) for i in range(1,6)]
for url in urls:
  res = requests.get(url)
  js1 = json.loads(res.text)
  asklist = dict(js1).get('AskList')
  for one in asklist:
    print('问：{}\n答：{}\n'.format(one['AskContentTitle'], one['ReplyList'][0]['ReplyContentTitle']))
