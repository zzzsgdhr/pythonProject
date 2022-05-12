import selenium.webdriver, time, re
from selenium.common.exceptions import WebDriverException


class NovelSpider():
  def __init__(self, url):
    self.homepage = url
    self.driver = selenium.webdriver.Chrome(path_of_chromedriver)
    self.page_list = []

  def __del__(self):
    self.driver.quit()

  def get_page_urls(self):
    homepage = self.homepage
    self.driver.get(homepage)
    self.driver.save_screenshot('screenshot.png')

    self.driver.implicitly_wait(5)
    elements = self.driver.find_elements_by_tag_name('a')

    for one in elements:
      page_url = one.get_attribute('href')

      pattern = '^http:\/\/book\.zhulang\.com\/\d{6}\/\d+\.html'
      if re.match(pattern, page_url):
        print(page_url)
        self.page_list.append(page_url)

  def looping_crawl(self):
    homepage = self.homepage
    filename = self.get_novel_name(homepage) + '.txt'
    self.get_page_urls()
    pages = self.page_list
    # print(pages)

    for page in pages:
      self.driver.get(page)
      print('Next page:')

      self.driver.implicitly_wait(3)
      title = self.driver.find_element_by_tag_name('h2').text
      res = self.driver.find_element_by_id('read-content')
      text = '\n' + title + '\n'
      for one in res.find_elements_by_xpath('./p'):
        text += one.text
        text += '\n'

      self.text_to_txt(text, filename)
      time.sleep(1)
      print(page + '\t\t\tis Done!')

  def get_novel_name(self, homepage):

    self.driver.get(homepage)
    self.driver.implicitly_wait(2)

    res = self.driver.find_element_by_tag_name('strong').find_element_by_xpath('./a')
    if res is not None and len(res.text) > 0:
      return res.text
    else:
      return 'novel'

  def text_to_txt(self, text, filename):
    if filename[-4:] != '.txt':
      print('Error, incorrect filename')
    else:
      with open(filename, 'a') as fp:
        fp.write(text)
        fp.write('\n')


if __name__ == '__main__':
  hp_url = input('输入小说“全部章节”页面：')

  path_of_chromedriver = 'your_path_of_chrome_driver'

  try:
    sp1 = NovelSpider(hp_url)
    sp1.looping_crawl()
    del sp1
  except WebDriverException as e:
    print(e.msg)
