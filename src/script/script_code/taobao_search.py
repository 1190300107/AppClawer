# addimporttouch
# addsleep
# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python
import datetime
import os.path
import time
from selenium.webdriver.common.by import By

from src.script.script_lib.log import Log
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

class connect:
    def __init__(self):
        caps={}
        caps["platformName"] = "Android"
        caps["devicesName"] = '127.0.0.1：62025'
        caps["appPackage"] = 'com.taobao.taobao'
        caps["appActivity"] = 'com.taobao.tao.welcome.Welcome'
        caps["ensureWebviewsHavePages"] = True
        driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
        self.caps = caps
        self.driver = driver
        time.sleep(8)
    def start(self):
        driver = self.driver
        TouchAction(driver).tap(x=550, y=1507).perform()
        time.sleep(5)
        TouchAction(driver).tap(x=395, y=266).perform()
        time.sleep(5)
        el2 = driver.find_element(By.ID,"com.taobao.taobao:id/searchEdit")
        el2.send_keys("篮球")

    def action(self):
        log = Log(timestamp=datetime.datetime.now().timestamp(),action=os.path.basename(__file__).split('.')[0])
        log.dump()
        TouchAction(self.driver).tap(x=1008, y=149).perform()
        time.sleep(5)
        self.driver.quit()
        time.sleep(3)
    def get_package(self):

        return self.caps['appPackage']
if __name__ == '__main__':
    for i in range(5):
        print(i)
        my_connect = connect()
        my_connect.start()
        my_connect.action()
        time.sleep(5)
        print(i)



