from selenium import webdriver
import time
from selenium.webdriver.common.by import By

browser = webdriver.Chrome('yourchromedriverpath')
browser.get('http://www.douban.com')
time.sleep(1)
search_box = browser.find_element(By.NAME,'q')
search_box.send_keys('网站开发')
button = browser.find_element(By.CLASS_NAME,'bn')
button.click()
