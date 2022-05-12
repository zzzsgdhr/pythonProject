from selenium import webdriver
from selenium.webdriver import ActionChains

path_of_chromedriver = 'your path of chrome driver'
driver = webdriver.Chrome(path_of_chromedriver)
driver.get('https://www.douban.com/login')
email_field = driver.find_element_by_id('email')
pw_field = driver.find_element_by_id('password')
submit_button = driver.find_element_by_name('login')

email_field.send_keys('youremail@mail.com')
pw_field.send_keys('yourpassword')
submit_button.click()
