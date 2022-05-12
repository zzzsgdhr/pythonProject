from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# 滚动页面
browser = webdriver.Chrome('your chrome diver path')
browser.get('https://news.baidu.com/')
print(browser.title) # 输出："百度一下，你就知道"
for i in range(20):
  # browser.execute_script("window.scrollTo(0,document.body.scrollHeight)") # 使用执行JS的方式滚动
  ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform() # 使用模拟键盘输入的方式滚动
  time.sleep(0.5)

browser.quit() # 退出
