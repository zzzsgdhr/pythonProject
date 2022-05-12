import requests
from requests.auth import HTTPBasicAuth

url = 'https://www.httpwatch.com/httpgallery/authentication/authenticatedimage/default.aspx'

auth = HTTPBasicAuth('httpwatch', 'pw123') # 将用户名和密码作为对象初始化的参数
resp = requests.post(url, auth=auth)

with open('auth-image.jpeg','wb') as f:
  f.write(resp.content)
