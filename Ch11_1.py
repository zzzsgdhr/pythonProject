import time, sys, re, os, requests, json, random
from lxml import html
from PIL import Image
from pprint import pprint

class DoubanSpider():
  _session = requests.Session()
  _douban_url = 'https://accounts.douban.com/login'
  _header_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, sdch, br',
                  'Connection': 'keep-alive',
                  'Cache-Control': 'max-age=0',
                  'Host': 'www.douban.com',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                  }
  _captcha_url = ''

  def __init__(self, nickname):
    self.initial()
    self._usernick = nickname

  def initial(self):
    if os.path.exists('cookiefile'):
      print('have cookies yet')
      self.read_cookies()
    else:
      self.login()

  def login(self):

    r = self._session.get('https://accounts.douban.com/login', headers=self._header_data)
    print(r.status_code)
    self.input_login_data()
    login_data = {'form_email': self.username, 'form_password': self.password, "login": u'登录',
                  "redir": "https://www.douban.com"}
    response1 = html.fromstring(r.content)

    if len(response1.xpath('//*[@id="captcha_image"]')) > 0:
      self._captcha_url = response1.xpath('//*[@id="captcha_image"]/@src')[0]
      print(self._captcha_url)
      self.show_an_online_img(url=self._captcha_url)
      captcha_value = input("输入图中的验证码")
      login_data['captcha-solution'] = captcha_value

    r = self._session.post(self._douban_url, data=login_data, headers=self._header_data)
    r_homepage = self._session.get('https://www.douban.com', headers=self._header_data)

    pprint(html.fromstring(r_homepage.content))
    self.save_cookies()

  def download_img(self, url, filename):
    header = self._header_data
    match = re.search('img\d\.doubanio\.com', url)
    header['Host'] = url[match.start():match.end()]

    print('Downloading')
    filepath = os.path.join(os.getcwd(), 'pics/{}.jpg'.format(filename))

    self.random_sleep()
    r = requests.get(url, headers=header)
    if r.ok:
      with open(filepath, 'wb') as f:
        f.write(r.content)
        print('Downloaded Done!')
    else:
      print(r.status_code)
    del r

    return filepath

  def show_an_online_img(self, url):
    path = self.download_img(url, 'online_img')
    img = Image.open(path)
    img.show()
    os.remove(path)

  def save_cookies(self):
    with open('./' + "cookiefile", 'w')as f:
      json.dump(self._session.cookies.get_dict(), f)

  def read_cookies(self):
    with open('./' + 'cookiefile')as f:
      cookie = json.load(f)
      self._session.cookies.update(cookie)

  def input_login_data(self):
    global email
    global password

    self.username = input('输入用户名(必须是注册时的邮箱):')
    self.password = input('输入密码:')

  def get_home_page(self):
    r = self._session.get('https://www.douban.com')
    h = html.fromstring(r.content)
    print(h.text_content())

  def get_movie_I_watched(self, maxpage):
    moviename_watched = []

    url_start = 'https://movie.douban.com/people/{}/collect'.format(self._usernick)
    lastpage_xpath = '//*[@id="content"]/div[2]/div[1]/div[3]/a[5]/text()'

    r = self._session.get(url_start, headers=self._header_data)
    h = html.fromstring(r.content)

    urls = \
      ['https://movie.douban.com/people/{}/collect?start={}&sort=time&rating=all&filter=all&mode=grid'.format(
        self._usernick, 15 * i) for i in range(0, maxpage)]
    for url in urls:
      r = self._session.get(url)
      h = html.fromstring(r.content)

      movie_titles = h.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div')
      for one in movie_titles:
        movie_name = one.xpath('./div[2]/ul/li[1]/a/em/text()')[0]
        movie_url = one.xpath('./div[1]/a/@href')[0]
        moviename_watched.append(self.text_cleaner(movie_name))
        self.download_movie_pic(movie_url, movie_name)
        self.random_sleep()

    return moviename_watched

  def download_movie_pic(self, movie_page_url, moviename):
    moviename = self.text_cleaner(moviename)
    movie_pics_page_url = movie_page_url + 'photos?type=R'
    print(movie_pics_page_url)

    xpath_exp = '//*[@id="content"]/div/div[1]/ul/li[1]/div[1]/a/img'

    response = self._session.get(movie_pics_page_url)
    h = html.fromstring(response.content)

    if len(h.xpath(xpath_exp)) > 0:
      pic_url = h.xpath(xpath_exp)[0].get('src')
      print(pic_url)
      self.download_img(pic_url, moviename)

  def text_cleaner(self, text):
    text = str(text).replace('\n', '').strip(' ').replace('\\n', '').replace('/', '-').replace(' ', '')
    return text

  def random_sleep(self):
    t = random.randrange(50, 200)
    t = float(t) / 100
    print("We will sleep for {} seconds".format(t))
    time.sleep(t)

  def get_book_I_read(self, maxpage):
    bookname_read = [()]

    urls = \
      ['https://book.douban.com/people/{}/collect?start={}&sort=time&rating=all&filter=all&mode=grid'.format(
        self._usernick, 15 * i)
        for i in range(0, maxpage)]

    for url in urls:
      r = self._session.get(url)
      h = html.fromstring(r.content)
      book_titles = h.xpath('//*[@id="content"]/div[2]/div[1]/ul/li')
      for one in book_titles:
        name = one.xpath('./div[2]/h2/a/text()')[0]
        base_info = one.xpath('./div[2]/div[1]/text()')[0]
        bookname_read.append((self.text_cleaner(name), self.text_cleaner(base_info)))

    return bookname_read

if __name__ == '__main__':
  nickname = input("输入豆瓣用户名，即个人主页地址中/people/后的部分：")
  maxpagenum = int(input("输入观影记录的最大抓取页数："))
  db = DoubanSpider(nickname)
  pprint(db.get_movie_I_watched(maxpagenum))
