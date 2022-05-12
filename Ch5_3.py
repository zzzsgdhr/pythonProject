import requests, pickle
from bs4 import BeautifulSoup
from pprint import pprint

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
sess = requests.Session()
with open('zhihu-cookies.pkl', 'rb') as f:
  cookie_data = pickle.load(f) # 加载cookie信息

for cookie in cookie_data:
  sess.cookies.set(cookie['name'], cookie['value']) # 为session设置cookie信息

res = sess.get('https://www.zhihu.com/settings/profile', headers=headers).text # 访问并获得页面信息
ht = BeautifulSoup(res, 'lxml')
# pprint(ht)
node = ht.find('div', {'id': 'js-url-preview'}) # 获得
print(node.text)
