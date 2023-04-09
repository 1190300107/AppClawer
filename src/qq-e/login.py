# This sample code uses the Appium python client v2
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python
import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

caps = {}
caps["platformName"] = "Android"
caps["appium:platformVersion"] = "12.0"
caps["appium:deviceName"] = "安卓虚拟机QQ"
caps["appium:appPackage"] = "com.tencent.mobileqq"
caps["appium:appActivity"] = ".activity.SplashActivity"
caps["appium:udid"] = "emulator-5554"
caps["appium:ensureWebviewsHavePages"] = True
caps["appium:nativeWebScreenshot"] = True
caps["appium:newCommandTimeout"] = 3600
caps["appium:connectHardwareKeyboard"] = True

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)

actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(960,1914)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.pause(0.1)
actions.w3c_actions.pointer_action.release()
actions.perform()
time.sleep(5)



actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(1064,2585)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.pause(0.1)
actions.w3c_actions.pointer_action.release()
actions.perform()

time.sleep(5)

el1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="请输入QQ号码或手机号或QID或邮箱")
el1.send_keys("289410265")
el1.click()
el2 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="密码 安全")
el2.send_keys("wzh52dd123")
el3 = driver.find_element(by=AppiumBy.ID, value="com.tencent.mobileqq:id/r3z")
el3.click()
el4 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="登 录")
el4.click()
time.sleep(10)
driver.quit()