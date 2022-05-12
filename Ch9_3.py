# 增加博客访问量
import re, random, requests, logging
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool

logging.basicConfig(level=logging.DEBUG)
TIME_OUT = 6  # 超时时间
count = 0
proxies = []
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/36.0.1985.125 Safari/537.36',
           }
PROXY_URL = 'http://www.xicidaili.com/'


def GetProxies():
   global proxies
   try:
      res = requests.get(PROXY_URL, headers=headers)
   except:
      logging.error('Visit failed')
      return

   ht = html.fromstring(res.text)
   raw_proxy_list = ht.xpath('//*[@id="ip_list"]/tbody/tr')
   for item in raw_proxy_list:
      if item.xpath('./td[6]/text()')[0] == 'HTTP':
         proxies.append(
            dict(
               http='{}:{}'.format(
                  item.xpath('./td[2]/text()')[0], item.xpath('./td[3]/text()')[0])
            )
         )


# 获取博客文章列表
def GetArticles(url):
   res = GetRequest(url, prox=None)
   html = res.content.decode('utf-8')
   rgx = '<li class="blog-unit">[ \n\t]*<a href="(.+?)"" target="_blank">'
   ptn = re.compile(rgx)
   blog_list = re.findall(ptn, str(html))
   return blog_list

def GetRequest(url, prox):
   req = requests.get(url, headers=headers, proxies=prox, timeout=TIME_OUT)
   return req

# 访问博客
def VisitWithProxy(url):
   proxy = random.choice(proxies)  # 随机选择一个代理
   GetRequest(url, proxy)

# 多次访问
def VisitLoop(url):
   for i in range(count):
      logging.debug('Visiting:\t{}\tfor {} times'.format(url, i))
      VisitWithProxy(url)


if __name__ == '__main__':
   global count

   GetProxies()  # 获取代理
   logging.debug('We got {} proxies'.format(len(proxies)))
   BlogUrl = input('Blog Address:').strip(' ')
   logging.debug('Gonna visit{}'.format(BlogUrl))
   try:
      count = int(input('Visiting Count:'))
   except ValueError:
      logging.error('Arg error!')
      quit()
   if count == 0 or count > 200:
      logging.error('Count illegal')
      quit()

   article_list = GetArticles(BlogUrl)
   if len(article_list) == 0:
      logging.error('No articles, eror!')
      quit()

   for each_link in article_list:
      if not 'https://blog.csdn.net' in each_link:
         each_link = 'https://blog.csdn.net' + each_link
      article_list.append(each_link)
   # 多线程
   pool = ThreadPool(int(len(article_list) / 4))
   results = pool.map(VisitLoop, article_list)
   pool.close()
   pool.join()
   logging.DEBUG('Task Done')
