import requests
from bs4 import BeautifulSoup

# 一个可以显示当前访问请求头区信息的网页
res = requests.get('https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending')
bs = BeautifulSoup(res.text)
# 定位到网页中的UA信息元素
td_list = [one.text for one in bs.find('table',{'class':'table'}).findChildren()]
print(td_list[-1])
