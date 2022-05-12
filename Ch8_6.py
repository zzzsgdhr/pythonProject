import unittest,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TestWikipedia(unittest.TestCase):
  path_of_chromedriver = 'your path of chromedriver'

  def setUp(self):
    self.driver = webdriver.Chrome(executable_path=TestWikipedia.path_of_chromedriver)

  def test_search_in_python_org(self):
    driver = self.driver
    driver.get("https://en.wikipedia.org/wiki/Main_Page")
    self.assertIn("Wikipedia", driver.title)
    elem = driver.find_element_by_name("search")
    elem.send_keys('Wikipedia')
    elem.send_keys(Keys.RETURN)
    time.sleep(3)
    assert "no results" not in driver.page_source

  def tearDown(self):
    print("Wikipedia test done.")
    self.driver.close()

if __name__ == "__main__":
  unittest.main()
