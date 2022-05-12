# 模拟浏览器通过滑动验证的程序示例，目标是在登录时通过滑动验证
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from PIL import Image

def get_screenshot(browser):
  browser.save_screenshot('full_snap.png')
  page_snap_obj = Image.open('full_snap.png')
  return page_snap_obj

# 在一些滑动验证中，获取背景图片可能需要更复杂的机制，
# 原始的HTML图片元素需要经过拼接整理才能拼出最终想要的效果
# 为了避免这样的麻烦，一个思路就是直接对网页截图，而不是去下载元素中的img src


def get_image(browser):
  img = browser.find_element_by_class_name('geetest_canvas_img')  # 根据元素class名定位
  time.sleep(2)
  loc = img.loc
  size = img.size

  left = loc['x']
  top = loc['y']
  right = left + size['width']
  bottom = top + size['height']

  page_snap_obj = get_screenshot(browser)
  image_obj = page_snap_obj.crop((left, top, right, bottom))
  return image_obj

# 获取滑动距离
def get_distance(image1, image2, start=57, thres=60, bias=7):
  # 比对RGB的值
  for i in range(start, image1.size[0]):
    for j in range(image1.size[1]):
      rgb1 = image1.load()[i, j]
      rgb2 = image2.load()[i, j]
      res1 = abs(rgb1[0] - rgb2[0])
      res2 = abs(rgb1[1] - rgb2[1])
      res3 = abs(rgb1[2] - rgb2[2])

      if not (res1 < thres and res2 < thres and res3 < thres):
        return i - bias
  return i - bias

# 计算滑动轨迹
def gen_track(distance):
  # 也可通过随机数来获得轨迹

  # 将滑动距离增大一点，即先滑过目标区域，再滑动回来，有助于避免被判定为机器人
  distance += 10
  v = 0
  t = 0.2
  forward = []

  current = 0
  mid = distance * (3 / 5)
  while current < distance:
    if current < mid:
      a = 2.35
      # 使用浮点数，避免机器人判定
    else:
      a = -3.35
    s = v * t + 0.5 * a * (t ** 2)  # 使用加速直线运动公式
    v = v + a * t
    current += s
    forward.append(round(s))

  backward = [-3, -2, -2, -2, ]

  return {'forward_tracks': forward, 'back_tracks': backward}


def crack_slide(browser):  # 破解滑动认证
  # 点击验证按钮，得到图片
  button = browser.find_element_by_class_name('geetest_radar_tip')
  button.click()
  image1 = get_image(browser)

  # 点击滑动，得到有缺口的图片
  button = browser.find_element_by_class_name('geetest_slider_button')
  button.click()
  # 获取有缺口的图片
  image2 = get_image(browser)
  # 计算位移量
  distance = get_distance(image1, image2)
  # 计算轨迹
  tracks = gen_track(distance)
  # 在计算轨迹方面，还可以使用一些鼠标采集工具事先采集人类用户的正常轨迹，将采集到的轨迹数据加载到程序中

  # 执行滑动
  button = browser.find_element_by_class_name('geetest_slider_button')
  ActionChains(browser).click_and_hold(button).perform()  # 点击并保持

  for track in tracks['forward']:
    ActionChains(browser).move_by_offset(xoffset=track, yoffset=0).perform()
  time.sleep(0.95)
  for back_track in tracks['backward']:
    ActionChains(browser).move_by_offset(xoffset=back_track, yoffset=0).perform()

  # 在滑动终点区域进行小范围的左右位移，模仿人类的行为
  ActionChains(browser).move_by_offset(xoffset=-2, yoffset=0).perform()
  ActionChains(browser).move_by_offset(xoffset=2, yoffset=0).perform()

  time.sleep(0.5)
  ActionChains(browser).release().perform()  # 松开

def worker(username, password):
  browser = webdriver.Chrome('your chrome driver path')
  try:
    browser.implicitly_wait(3)  # 隐式等待
    browser.get('your target login url')

    # 在实际使用时需要根据当前网页的情况定位元素
    username = browser.find_element_by_id('username')
    password = browser.find_element_by_id('password')
    login = browser.find_element_by_id('login')
    username.send_keys(username)
    password.send_keys(password)
    login.click()

    crack_slide(browser)

    time.sleep(15)
  finally:
    browser.close()

if __name__ == '__main__':
  worker(username='yourusername', password='yourpassword')
