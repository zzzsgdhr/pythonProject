import requests
from bs4 import BeautifulSoup

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
form_data = {'username': 'yourname',  # 用户名
             'password': 'yourpw',  # 密码
             'quickforward': 'yes',  # 对普通用户隐藏的字段，该值不需要用户主动设定
             'handlekey': 'ls'}  # 对普通用户隐藏的字段，该值不需要用户主动设定

session = requests.Session()  # 使用requests的session来保持会话状态
session.post(
  'http://www.1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1',
  headers=headers, data=form_data)
resp = session.get('http://www.1point3acres.com/bbs/').text
ht = BeautifulSoup(resp, 'lxml') # 根据访问得到的网页数据建立BeautifulSoup对象
cds = ht.find('div', {'class': 'avt y'}).findChildren() # 获取"<div class="avt y">元素节点下的孩子元素"
print(cds)
# 获取img src中的图片地址
img_src_links = [one.find('img')['src'] for one in cds if one.find('img') is not None]

for src in img_src_links:
  img_content = session.get(src).content
  src = src.lstrip('http://').replace(r'/', '-') # 将图片地址稍作处理并作为文件名
  with open('{src}.jpg'.format_map(vars()), 'wb+') as f:
    f.write(img_content) # 写入文件
