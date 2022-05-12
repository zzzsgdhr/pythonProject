import requests
import datetime
import multiprocessing as mp

def crawl(url, data): # 访问
  text = requests.get(url=url, params=data).text
  return text

def func(page): # 执行抓取
  url = "https://book.douban.com/subject/4117922/comments/hot"
  data = {
    "p": page
  }
  text = crawl(url, data)
  print("Crawling : page No.{}".format(page))

if __name__ == '__main__':

  start = datetime.datetime.now()
  start_page = 1
  end_page = 15

  # 多进程抓取
  # pages = [i for i in range(start_page, end_page)]
  # p = mp.Pool()
  # p.map_async(func, pages)
  # p.close()
  # p.join()


  # 单进程抓取
  page = start_page

  for page in range(start_page, end_page):
    url = "https://book.douban.com/subject/4117922/comments/hot"
    # get参数
    data = {
      "p": page
    }
    content = crawl(url, data)
    print("Crawling : page No.{}".format(page))

  end = datetime.datetime.now()
  print("Time\t: ", end - start)
