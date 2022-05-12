import threading
import time
from queue import Queue

que = Queue()
THREAD_NUM = 8  # 线程的个数

class WorkThread(threading.Thread):
   def __init__(self, func):
      super(WorkThread, self).__init__()  # 调用父类的构造函数
      self.func = func  # 设置工作函数

   def run(self):
      """
      重写基类的run方法

      """
      self.func()

def crawl(item):
   """
   运行抓取
   """
   pass

def worker():
   """
   只要队列不空持续处理
   """
   global que
   while not que.empty():
      item = que.get()  # 获得任务
      crawl(item) # 抓取
      time.sleep(1) # 等待
      que.task_done()

def main():
   global que
   threads = []
   tasklist = []
   # 队列中添加任务
   for task in tasklist:
      que.put(task)

   for i in range(THREAD_NUM):
      thread = WorkThread(worker)
      threads.append(thread)
   for thread in threads:
      thread.start()  # 线程开始处理任务
      thread.join()
   # 等待所有任务完成
   que.join()

if __name__ == '__main__':
   main()
