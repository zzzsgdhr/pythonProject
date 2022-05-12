from lxml import html
import requests
from pprint import pprint
import smtplib
from email.mime.text import MIMEText
import time, logging, random
import os

class Mail163():
  _sendbox = 'yourmail@mail.com'
  _receivebox = ['receive@mail.com']
  _mail_password = 'password'
  _mail_host = 'server.smtp.com'
  _mail_user = 'yourusername'
  _port_number = 465 # 465 is default the port number for smtp server

  def SendMail(self, subject, body):
    print("Try to send...")
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = self._sendbox
    msg['To'] = ','.join(self._receivebox)
    try:
      smtpObj = smtplib.SMTP_SSL(self._mail_host, self._port_number)  # get the server
      smtpObj.login(self._mail_user, self._mail_password)  # login in
      smtpObj.sendmail(self._sendbox, self._receivebox, msg.as_string())  # send the mail
      print('Sent successfully')
    except:
      print('Sent failed')


# Global Vars
header_data = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate, sdch, br',
  'Accept-Language': 'zh-CN,zh;q=0.8',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
}
url_list = [
  'http://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=82&sortid=164&%1=&sortid=164&page={}'.format(i) for i
  in range(1, 5)]
url = 'http://www.1point3acres.com/bbs/forum-82-1.html'
mail_sender = Mail163()
shit_words = ['PhD', 'MFE', 'Spring', 'EE', 'Stat', 'ME', 'Other']
DONOTCARE = 'DONOTCARE'
DOCARE = 'DOCARE'
PWD = os.path.abspath(os.curdir)
RECORDTXT = os.path.join(PWD, 'Record-Titles.txt')
ses = requests.Session()


def SentenceJudge(sent):
  for word in shit_words:
    if word in sent:
      return DONOTCARE

  return DOCARE


def RandomSleep():
  float_num = random.randint(-100, 100)
  float_num = float(float_num / (100))
  sleep_time = 5 + float_num
  time.sleep(sleep_time)
  print('Sleep for {} s.'.format(sleep_time))


def SendMailWrapper(result):
  mail_subject = 'New AD/REJ @ 一亩三分地: {}'.format(result[0])
  mail_content = 'Title:\t{}\n' \
                 'Link:\n{}\n' \
                 '{} in\n' \
                 '{} of\n' \
                 '{}\n' \
                 'Date:\t{}\n' \
                 '---\nSent by Python Toolbox.' \
    .format(result[0], result[1], result[3], result[4], result[5], result[6])

  mail_sender.SendMail(mail_subject, mail_content)


def RecordWriter(title):
  with open(RECORDTXT, 'a') as f:
    f.write(title + '\n')
  logging.debug("Write Done!")

def RecordCheckInList():
  checkinlist = []
  with open(RECORDTXT, 'r') as f:
    for line in f:
      checkinlist.append(line.replace('\n', ''))

  return checkinlist

def Parser():
  final_list = []
  for raw_url in url_list:
    RandomSleep()
    pprint(raw_url)
    r = ses.get(raw_url, headers=header_data)
    text = r.text
    ht = html.fromstring(text)
    for result in ht.xpath('//*[@id]/tr/th'):
      # pprint(result)
      # pprint('------')
      content_title = result.xpath('./a[2]/text()')  # 0
      content_link = result.xpath('./a[2]/@href')  # 1
      content_semester = result.xpath('./span[1]/u/font[1]/text()')  # 2
      content_degree = result.xpath('./span[1]/u/font[2]/text()')  # 3
      content_major = result.xpath('./span/u/font[4]/b/text()')  # 4
      content_dept = result.xpath('./span/u/font[5]/text()')  # 5
      content_releasedate = result.xpath('./span/font[1]/text()')  # 6

      if len(content_title) + len(content_link) >= 2 and content_title[0] != '预览':
        final = []
        final.append(content_title[0])
        final.append(content_link[0])

        if len(content_semester) > 0:
          final.append(content_semester[0][1:])
        else:
          final.append('No Semester Info')
        if len(content_degree) > 0:
          final.append(content_degree[0])
        else:
          final.append('No Degree Info')
        if len(content_major) > 0:
          final.append(content_major[0])
        else:
          final.append('No Major Info')
        if len(content_dept) > 0:
          final.append(content_dept[0])
        else:
          final.append('No Dept Info')
        if len(content_releasedate) > 0:
          final.append(content_releasedate[0])
        else:
          final.append('No Date Info')
        # print('Now :\t{}'.format(final[0]))
        if SentenceJudge(final[0]) != DONOTCARE and \
                        SentenceJudge(final[3]) != DONOTCARE and \
                        SentenceJudge(final[4]) != DONOTCARE and \
                        SentenceJudge(final[2]) != DONOTCARE:
          final_list.append(final)
      else:
        pass

  return final_list

if __name__ == '__main__':

  print("Record Text Path:\t{}".format(RECORDTXT))
  final_list = Parser()
  pprint('final_list:\tThis time we have these results:')
  pprint(final_list)
  print('*' * 10 + '-' * 10 + '*' * 10)
  sent_list = RecordCheckInList()
  pprint("sent_list:\tWe already sent these:")
  pprint(sent_list)
  print('*' * 10 + '-' * 10 + '*' * 10)
  for one in final_list:
    if one[0] not in sent_list:
      pprint(one)
      SendMailWrapper(one) # Send this new post
      RecordWriter(one[0])  # Write New into The RECORD TXT
      RandomSleep()

  RecordWriter('-' * 15)

  del mail_sender
  del final_list
  del sent_list
