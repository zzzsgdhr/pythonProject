import itchat
from collections import Counter
import matplotlib.pyplot as plt
import csv
from pprint import pprint


def anaSex(friends):
  sexs = list(map(lambda x: x['Sex'], friends[1:]))
  counts = list(map(lambda x: x[1], Counter(sexs).items()))
  labels = ['Unknow', 'Male', 'Female']
  colors = ['Grey', 'Blue', 'Pink']
  plt.figure(figsize=(8, 5), dpi=80) # 调整绘图大小
  plt.axes(aspect=1)
  # 绘制饼图
  plt.pie(counts,
          labels=labels,
          colors=colors,
          labeldistance=1.1,
          autopct='%3.1f%%',
          shadow=False,
          startangle=90,
          pctdistance=0.6
          )
  plt.legend(loc='upper right',)
  plt.title('The gender distribution of {}\'s WeChat Friends'.format(friends[0]['NickName']))
  plt.show()

def anaLoc(friends):
  headers = ['NickName', 'Province', 'City']
  with open('location.csv', 'w', encoding='utf-8', newline='', ) as csvFile:
    writer = csv.DictWriter(csvFile, headers)
    writer.writeheader()
    for friend in friends[1:]:
      row = {}
      row['NickName'] = friend['RemarkName']
      row['Province'] = friend['Province']
      row['City'] = friend['City']
      writer.writerow(row)

if __name__ == '__main__':

  itchat.auto_login(hotReload=True)
  friends = itchat.get_friends(update=True)
  anaSex(friends)
  anaLoc(friends)
  pprint(friends)
  itchat.logout()
