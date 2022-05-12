from selenium import webdriver
import time

browser = webdriver.Chrome('yourchromedriverpath')
# 如"/home/zyang/chromedriver"
browser.get('http:www.baidu.com')
print(browser.title) # 输出："百度一下，你就知道"
browser.find_element_by_name("tj_trnews").click() # 点击"新闻"
browser.find_element_by_class_name('hdline0').click() # 点击头条
print(browser.current_url) # 输出：http://news.baidu.com/
time.sleep(10)
browser.quit() # 退出
