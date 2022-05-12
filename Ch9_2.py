import requests
from bs4 import BeautifulSoup

header_data = {
  'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
}

r = requests.get('https://tieba.baidu.com',headers=header_data)

bs = BeautifulSoup(r.content)
with open('h2.html', 'wb') as f:
  f.write(bs.prettify(encoding='utf8'))
