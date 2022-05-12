import requests
import time
import os

# 原始数据获取URL
raw_url = 'https://www.bilibili.com/index/recommend.json'
# 根据开发者工具中的request header信息来设置headers
headers = {
  'Host':'www.bilibili.com',
  'X-Requested-With': 'XMLHttpRequest',
  'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
}


def save_image(url):
  filename = url.lstrip('http://').replace('.', '').replace('/', '').rstrip('jpg')+'.jpg'
  # 将图片地址转化为图片文件名
  try:
    res = requests.get(url, headers=headers)
    if res.ok:
      img = res.content
      if not os.path.exists(filename): # 检查该图片是否已经下载过
        with open(filename, 'wb') as f:
          f.write(img)
  except Exception:
    print('Failed to load the picture')


def get_json():
  try:
    res = requests.get(raw_url, headers=headers)
    if res.ok:  # 成功访问
      return res.json()  # 返回json
    else:
      print('not ok')
      return False
  except Exception as e:
    print('Error here:\t', e)


# JSON数据处理
def json_parser(json):
  if json is not None:
    news_list = json.get('list')
    if not news_list:
      return False
    for news_item in news_list:
      pic_url = news_item.get('pic')
      yield pic_url  # 使用生成器yield方法

def worker():
  raw_json = get_json()  # 获取原始JSON数据
  print(raw_json)
  urls = json_parser(raw_json)
  for url in urls:
    save_image(url)

if __name__ == '__main__':
  worker()
