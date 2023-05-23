# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
import sys
import time as Time
import subprocess
import re
from datetime import datetime
from difflib import SequenceMatcher
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
import xml.etree.ElementTree as ET
from xmldiff import main
import yaml
import traceback
from vk import input_all,input_word
sys.path.append('../../')
from lib.exception.originexception import Origin_exception
caps = {}
caps["platformName"] = "Android"
caps["devicesName"] = '127.0.0.1：62025'

caps["ensureWebviewsHavePages"] = True
level = -1
MAX_LEVEL = 5
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
driver.implicitly_wait(300)
def input_all():
    try:
        edit_text_list = driver.find_elements(By.XPATH,'.//android.widget.EditText')
        print(f'获取到输入框:')
        print(edit_text_list)
    except:
        print('input_all error')
        traceback.print_exc()
    for i in range(len(edit_text_list)):
        input(edit_text_list[i])

def input_word(edit_text:webdriver.webelement.WebElement,word='123456'):
    """
    根据word填充到edit_text中
    :param edit_text:
    :param word:
    :return:
    """
    try:
        print('尝试将{word}填充')
        print(f'{edit_text}')
        edit_text.send_keys(word)
    except:
        print('input_word error')
        traceback.print_exc()
if __name__ == '__main__':
    input_all()