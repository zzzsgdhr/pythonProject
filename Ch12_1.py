import jieba, numpy, re, time, matplotlib, requests, logging, snownlp, threading
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from queue import Queue

matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
matplotlib.rcParams['font.serif'] = ['KaiTi']

HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
           }
NOW_PLAYING_URL = 'https://movie.douban.com/nowplaying/beijing/'
logging.basicConfig(level=logging.DEBUG)


class MyThread(threading.Thread):
   CommentList = []
   Que = Queue()

   def __init__(self, i, MovieID):
      super(MyThread, self).__init__()
      self.name = '{}th thread'.format(i)
      self.movie = MovieID

   def run(self):
      logging.debug('Now running:\t{}'.format(self.name))
      while not MyThread.Que.empty():
         page = MyThread.Que.get()
         commentList_temp = GetCommentsByID(self.movie, page + 1)
         MyThread.CommentList.append(commentList_temp)
         MyThread.Que.task_done()


def MovieURLtoID(url):
   res = int(re.search('(\D+)(\d+)(\/)', url).group(2))
   return res

def GetCommentsByID(MovieID, PageNum):
   result_list = []
   if PageNum > 0:
      start = (PageNum - 1) * 20
   else:
      logging.error('PageNum illegal!')
      return False

   url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20'.format(MovieID, str(start))
   logging.debug('Handling :\t{}'.format(url))
   resp = requests.get(url,headers=HEADERS)
   html = resp.content.decode('utf-8')
   bs = BeautifulSoup(html, 'html.parser')
   div_list = bs.find_all('div', class_='comment')

   for item in div_list:
      if item.find_all('p')[0].string is not None:
         result_list.append(item.find_all('p')[0].string)
   time.sleep(2) # Pause for several seconds
   return result_list


def DFGraphBar(df):
   df.plot(kind="bar", title='Words Freq', x='seg', y='freq')
   plt.show()


def WordFrequence(MaxPage=15, ThreadNum=8, movie=None):
   # 循环获取电影的评论
   if not movie:
      logging.error('No movie here')
      return
   else:
      MovieID = movie

   for page in range(MaxPage):
      MyThread.Que.put(page)

   threads = []
   for i in range(ThreadNum):
      work_thread = MyThread(i, MovieID)
      work_thread.setDaemon(True)
      threads.append(work_thread)
   for thread in threads:
      thread.start()

   MyThread.Que.join()
   CommentList = MyThread.CommentList

   comments = ''
   for one in range(len(CommentList)):
      new_comment = (str(CommentList[one])).strip()
      new_comment = re.sub('[-\\ \',\.n（）#…/\n\[\]!~]', '', new_comment)
      # 使用正则表达式清洗文本，主要是去除一些标点
      comments = comments + new_comment

   pprint(SumOfComment(comments)) # 输出文本摘要
   # 中文分词
   segments = jieba.lcut(comments)
   WordDF = pd.DataFrame({'seg': segments})

   # 去除停用词
   stopwords = pd.read_csv("stopwordsChinese.txt",
                           index_col=False,
                           names=['stopword'],
                           encoding='utf-8')

   WordDF = WordDF[~WordDF.seg.isin(stopwords.stopword)]  # 取反

   # 统计词频
   WordAnal = WordDF.groupby(by=['seg'])['seg'].agg({'freq': numpy.size})
   WordAnal = WordAnal.reset_index().sort_values(by=['freq'], ascending=False)
   WordAnal = WordAnal[0:40]  # 仅取前40个高频词

   print(WordAnal)
   return WordAnal


def SumOfComment(comment):
   s = snownlp.SnowNLP(comment)
   sum = s.summary(5)
   return sum

# 执行函数
if __name__ == '__main__':
   DFGraphBar(WordFrequence(movie=MovieURLtoID('https://movie.douban.com/subject/1291575/')))
