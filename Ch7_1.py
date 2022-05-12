from selenium import webdriver
import selenium.webdriver, time, re
from selenium.common.exceptions import WebDriverException
import logging
import matplotlib.pyplot as pyplot
from collections import Counter

path_of_chromedriver = 'your path of chromedriver'
driver = webdriver.Chrome(executable_path=path_of_chromedriver)
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == '__main__':

  try:
    driver.get('https://wx.qq.com')
    time.sleep(20)  # waiting for scanning QRcode and open the GroupChat page
    logging.debug('Starting traking the webpage')
    group_elem = driver.find_element_by_xpath('//*[@id="chatArea"]/div[1]/div[2]/div/span')
    group_elem.click()
    group_num = int(str(group_elem.text)[1:-1])
    # group_num = 64
    logging.debug('Group num is {}'.format(group_num))

    gender_dict = {'MALE': 0, 'FEMALE': 0, 'NULL': 0}
    for i in range(2, group_num + 2):
      logging.debug('Now the {}th one'.format(i-1))
      icon = driver.find_element_by_xpath('//*[@id="mmpop_chatroom_members"]/div/div/div[1]/div[%s]/img' % i)
      icon.click()
      gender_raw = driver.find_element_by_xpath('//*[@id="mmpop_profile"]/div/div[2]/div[1]/i').get_attribute('class')
      if 'women' in gender_raw:
        gender_dict['FEMALE'] += 1
      elif 'men' in gender_raw:
        gender_dict['MALE'] += 1
      else:
        gender_dict['NULL'] += 1

      myicon = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/div[1]/img')
      logging.debug('Now click my icon')
      myicon.click()
      time.sleep(0.7)
      logging.debug('Now click group title')
      group_elem.click()
      time.sleep(0.3)

    print(gender_dict)
    print(gender_dict.items())
    counts = Counter(gender_dict)

    pyplot.pie([v for v in counts.values()],
               labels=[k for k in counts.keys()],
               pctdistance=1.1,
               labeldistance=1.2,
               autopct='%1.0f%%')
    pyplot.show()

  except WebDriverException as e:
    print(e.msg)
