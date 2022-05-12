from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert

browser = webdriver.Chrome('yourchromedriverpath')
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
# 切换到一个frame
browser.switch_to.frame('iframeResult') #
# 不推荐browser.switch_to_frame()方法
# 根据id定位元素
source = browser.find_element_by_id('draggable') # 被拖拽区域
target = browser.find_element_by_id('droppable') # 目标区域
ActionChains(browser).drag_and_drop(source, target).perform() # 执行动作链
alt = Alert(browser)
print(alt.text) # 输出："dropped"
alt.accept() # 接受弹出框
