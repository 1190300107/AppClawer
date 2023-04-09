# addimporttouch
# addsleep
# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from time import sleep
caps = {}
caps["platformName"] = "Android"
caps["ensureWebviewsHavePages"] = True
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)

time.sleep(10)#等待10秒，跳过微博启动时的广告
TouchAction(driver).tap(x=113, y=2063).perform()#点击左下角主页按钮
sleep(3)#等待3秒，用于页面更新的时间
TouchAction(driver).tap(x=112, y=2057).perform()#点击左下角主页按钮
sleep(3)#等待3秒，用于页面更新的时间
TouchAction(driver).tap(x=109, y=2063).perform()#点击左下角主页按钮
sleep(3)#等待3秒，用于页面更新的时间

driver.quit()