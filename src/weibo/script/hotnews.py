# addimporttouch
# addsleep
# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python
import time
from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver
from time import sleep

caps = {}
caps["platformName"] = "Android"
caps["ensureWebviewsHavePages"] = True

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
TouchAction(driver).tap(x=532, y=2041).perform()
sleep(3)
TouchAction(driver).tap(x=120, y=544).perform()
sleep(3)
driver.back()
TouchAction(driver).tap(x=705, y=539).perform()
sleep(3)
driver.back()
TouchAction(driver).tap(x=232, y=504).perform()
sleep(3)
driver.back()
TouchAction(driver).tap(x=688, y=504).perform()
sleep(3)
driver.back()

sleep(5)
driver.quit()