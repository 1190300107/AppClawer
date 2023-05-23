# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
# @Time    : 2022/12/6 19:54
import os
def addsleep(filelist:[str]):
    for file in filelist:
        with open(file, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            if '# addsleep\n' in lines:
                continue
            newlines = []
            for line in lines:
                newlines.append(line)
                if 'tap' in line:
                    newlines.append('sleep(3)\n')
        newlines.insert(5,'from time import sleep\n')
        newlines.insert(-1,'sleep(5)\n')
        newlines.insert(0,'# addsleep\n')
        with open(file, 'w+', encoding='utf-8') as f:
            f.writelines(newlines)
def addimporttouch(filelist:[str]):
    for file in filelist:
        with open(file, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            if '# addimporttouch\n' in lines:
                continue
        newlines = lines
        newlines.insert(5,'from appium.webdriver.common.touch_action import TouchAction\n')
        newlines.insert(0,'# addimporttouch\n')
        with open(file, 'w+', encoding='utf-8') as f:
            f.writelines(newlines)
