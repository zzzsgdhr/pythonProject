import selenium.webdriver
import pickle, time, os


class SeleZhihu():
  _path_of_chromedriver = 'chromedriver'
  _browser = None
  _url_homepage = 'https://www.zhihu.com/'
  _cookies_file = 'zhihu-cookies.pkl'
  _header_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, sdch, br',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Connection': 'keep-alive',
                  'Cache-Control': 'max-age=0',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                  }

  def __init__(self):
    self.initial()

  def initial(self):
    self._browser = selenium.webdriver.Chrome(self._path_of_chromedriver)
    self._browser.get(self._url_homepage)

    if self.have_cookies_or_not():
      self.load_cookies()
    else:
      print('Login first')
      time.sleep(30)
      self.save_cookies()

    print('We are here now')

  def have_cookies_or_not(self):
    if os.path.exists(self._cookies_file):
      return True
    else:
      return False

  def save_cookies(self):
    pickle.dump(self._browser.get_cookies(), open(self._cookies_file, "wb"))
    print("Save Cookies successfully!")

  def load_cookies(self):
    self._browser.get(self._url_homepage)
    cookies = pickle.load(open(self._cookies_file, "rb"))
    for cookie in cookies:
      self._browser.add_cookie(cookie)
    print("Load Cookies successfully!")

  def get_page_by_url(self, url):
    self._browser.get(url)

  def quit_browser(self):
    self._browser.quit()


if __name__ == '__main__':
  zh = SeleZhihu()
  zh.get_page_by_url('https://www.zhihu.com/')

  time.sleep(10)
  zh.quit_browser()
