import requests
from bs4 import BeautifulSoup

# url = 'http://localhost:8050/render.html?url=https://www.jd.com'
url = 'https://www.jd.com'
resp = requests.get(url)
html = resp.text
ht = BeautifulSoup(html)
print(ht.find(id='J_event_lk').get('href')) # 根据开发者工具分析得到元素id
