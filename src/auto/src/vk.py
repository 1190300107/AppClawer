# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
# @Time    : 2023/3/19 22:09
import datetime
import re
import time
from difflib import SequenceMatcher
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
import traceback

caps = {}
caps["platformName"] = "Android"
caps["devicesName"] = '127.0.0.1：62025'

caps["ensureWebviewsHavePages"] = True
level = -1
MAX_LEVEL = 2
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
driver.implicitly_wait(3)

old_click_by_text_set=set()#根据按钮text记录当前元素是否遍历过，防止重复遍历
# old_xml_set = set()
black_list_content_desc = ['back']
black_element_by_parse_text = []


def init_black_element():
    """
    读取./config/black_element_by_parse_text.txt，初始化按钮黑名单
    :return:
    """
    global black_element_by_parse_text
    with open('../config/black_element_by_parse_text.txt',encoding='utf8') as f:
        black_list = f.readlines()
        for item in black_list:
            black_element_by_parse_text.append(eval(item))
    print('black_element_by_parse_text:', black_element_by_parse_text)


def is_black(text_list) -> bool:
    # print(element.get_attribute('content-desc'))
    # try:
    #     content_desc = element.get_attribute('content-desc').lower()
    #     if content_desc in black_list_content_desc:
    #         print('content-desc',content_desc,'is black')
    #         return True
    # except:
    #     pass
    if text_list in black_element_by_parse_text:
        return True
    return False
def is_old(text_list)->bool:

    if str(text_list) in old_click_by_text_set:
        return True
    return False

def contain_text(element: webdriver.webelement.WebElement) -> bool:
    """
    判断按钮包含text
    :param element:
    :return: 包含则返回ture
    """
    try:
        text_click = element.find_elements(By.XPATH, './/*[@text!=""]')
    except:
        print('contain_text failed')
        return False
    return len(text_click) > 0





def parse_text_list(element: webdriver.webelement.WebElement):
    """
    提取元素中的所有text
    :param element:
    :return:
    """
    try:
        # text_click_list = [element.find_element(By.XPATH, './/*[@text!=""]')]
        text_click_list = [element.tag_name]
    except Exception as e:
        if 'Message: An element could not be located on the page using the given search param' in str(e):
            print('元素不包含文字')
            return []
        else:
            print('遇到新异常')
            raise e
    else:
        if len(text_click_list) == 0:
            return []
        else:
            text_list = []
            for click in text_click_list:
                try:
                    text = click.text
                except:
                    continue
                else:
                    text_list.append(text)
            return text_list


def dif(str1, str2):
    print(SequenceMatcher(None, str1, str2).quick_ratio())
    return SequenceMatcher(None, str1, str2).quick_ratio()


def is_same(str1,click_list_num1, str2,click_list_num2):
    print('click_list_num1:',click_list_num1)
    print('click_list_num2:',click_list_num2)
    return dif(str1,str2) >0.95 and (abs(click_list_num1-click_list_num2) <=2 or click_list_num1 ==0 or click_list_num2 ==0 )

def is_good_click(text_list):
    """
    遍历界面的element时候，判断element是否遍历过或者在黑名单那里
    :param element:
    :return:
    """
    if len(text_list) ==0:
        print(text_list,'is empty! bad!')
        return False
    elif is_old(text_list):
        print(text_list,'is old! bad!')
        return False
    elif is_black(text_list):
        print(text_list,'is black! bad!')
        return False
    else:
        print(text_list,'is good! Just do it!')
        return True
def search_element():
    """
    通过content-desc属性获取元素，后期根据坐标tap
    :return:
    """
    element_list = driver.find_elements(By.XPATH,'.//*[@text!=""]')
    return element_list
def judge_action_by_text_list(text_list:[str]):
    key_word = text_list[0]
    regex_action_map = {}
    regex_action_map[r'\d+$'] = '点击纯数字'
    for regex,action in regex_action_map.items():
        pattern = re.compile(regex)
        if pattern.match(key_word):
            print(key_word,'命中规则:',regex,'判定行为:',action)
            print(datetime.datetime.now())
            print(datetime.datetime.now().timestamp())
def parse_info_from_click(clicklist:[webdriver.webelement.WebElement]):
    """
    为了防止回溯之后，按钮丢失，将的上的text，location记录下载，后续根据这个记录去遍历，而不是根据原始的
    :param clicklist:
    :return:
    """
    pass
def dfs_2(enter_text_list,parent_page,parent_click_list_num,grandparent_page,grandparent_click_list_num) ->int:
    """
        深度优先搜索,退出时退回到parent_page或者grandparent_page

    :param parent_page:
    :param parent_click_list_num:
    :param grandparent_page:
    :param grandparent_click_list_num:
    :return:
    0==达到最大层数
    2==点击过程中意外回到父界面
    3==正常遍历完所有按钮
    4==点击过程中意外回到爷爷界面，孙子告诉孙子的父亲
    5==点击过程中意外回到爷爷界面，孙子的父亲告诉爷爷
    """
    global level
    global MAX_LEVEL
    global old_click_by_text_set
    level = level + 1
    print('\t' * level, 'level=', {level})

    if level == MAX_LEVEL:
        print('到达最大层数,返回')
        for i in range(MAX_LEVEL * 2 + 1):
            new_page = driver.page_source
            # new_click_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')
            new_click_list = search_element()
            time.sleep(2)
            if i == MAX_LEVEL * 2:
                print('多次返回仍无法回到父界面,测试崩溃,将该界面入口元素标记为黑名单')
                time.sleep(2)
                with open('../config/black_element_by_parse_text.txt', encoding='utf8', mode='a+') as f:
                    f.write(str(enter_text_list) + '\n')
                    exit(f'{enter_text_list}被收录至black_element_by_parse_text.txt')
            if is_same(new_page, len(new_click_list), parent_page, parent_click_list_num):
                print('返回父界面成功')
                break
            elif is_same(new_page, len(new_click_list), grandparent_page, grandparent_click_list_num):
                print(f'意外回退到{enter_text_list}的爷爷界面')
                code = 4
                level = level - 1
                print('level=', level)
                return code
            else:
                i = i + 1
                print(f'第{i}次尝试从{enter_text_list}返回父界面')
                driver.back()
                time.sleep(2)
        level = level - 1
        print('level=',level)
        code = 0
        return code
    else:#未达到最大层数，开始提取元素，遍历界面
        current_page = driver.page_source
        print('正在提取页面元素信息...')
        # current_click_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')
        current_click_list = search_element()
        print('页面元素提取成功!')

        for i,click in enumerate (current_click_list):
            print('正在遍历',enter_text_list,'界面的第',i+1,'个按钮')
            try:
                # text_list = [click.tag_name]
                text_list = []
                text = click.get_attribute('text')
                text_list.append(text)
                print('当前按钮文字列表为',text_list)
            except Exception as e:
                print(str(e))
                continue
            else:
                if not is_good_click(text_list):
                    continue
                print('click on ', text_list)
                judge_action_by_text_list(text_list)
                try:
                    click.click()
                except:
                    print(f'元素丢失', {text_list})
                    continue
                else:
                    old_click_by_text_set.add(str(text_list))
                    time.sleep(1)
                    new_page = driver.page_source
                    # new_click_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')
                    new_click_list = search_element()
                    if (dif(new_page, current_page) > 0.98):
                        current_page = new_page
                        print('点击无反应,忽略')
                        continue
                    elif is_same(new_page, len(new_click_list),parent_page,parent_click_list_num):
                        print('意外回退到父界面，将错就错，停止')
                        level = level - 1
                        code =2
                        return code
                    elif is_same(new_page, len(new_click_list), grandparent_page, grandparent_click_list_num):
                        print(f'意外回退到{text_list}的爷爷界面')
                        code = 4
                        level = level - 1
                        print('level=', level)
                        return code
                    else:
                        print('进入新界面', text_list)
                        code_child = dfs_2(text_list,current_page,len(current_click_list),parent_page,parent_click_list_num)#子dfs返回时，已经保证回退到进入dfs之前click之前的页面（即current_page），或者parent_page
                        if code_child ==4:#子界面遍历过程中意外跳转到爷爷界面,需要在此界面直接return，同时告知爷爷界面。
                            level = level -1
                            print('level=',level)
                            code =5
                            return code
                        elif code_child ==5:
                            print('孙子界面意外跳转到本爷爷界面==',enter_text_list)
                            # current_click_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')#重新更新爷爷界面list，否则总丢失元素，不用担心重复遍历，因为有记录old_click_by_text_set
                            continue
                        elif code_child==2:#子界面遍历的过程中意外跳转到父界面(即当前current_page)
                            # current_click_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')#重新更新父界面list，否则总丢失元素，不用担心重复遍历，因为有记录old_click_by_text_set
                            print('儿子界面意外跳转到本父亲界面==',enter_text_list)
                            continue
                        elif code_child ==0:
                            print('儿子界面达到最大层数，直接返回到本父亲界面==',enter_text_list)
                        elif code_child ==3:
                            print('儿子界面所有文字按钮已经遍历完毕，正常返回本父亲界面==',enter_text_list)

        print('当前界面==',enter_text_list,'所有文字按钮已经遍历完毕')
    for i in range(MAX_LEVEL * 2 + 1):
        new_page = driver.page_source
        # new_click_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')
        new_click_list = search_element()
        time.sleep(2)
        if i == MAX_LEVEL * 2:
            print('多次返回仍无法回到父界面,测试崩溃,将该界面入口元素标记为黑名单')
            time.sleep(2)
            with open('../config/black_element_by_parse_text.txt',encoding='utf8',mode='a+') as f:
                f.write(str(enter_text_list) + '\n')
                exit(f'{enter_text_list}被收录至black_element_by_parse_text.txt')
        if is_same(new_page, len(new_click_list), parent_page, parent_click_list_num):
            print('返回父界面成功')
            break
        elif is_same(new_page,len(new_click_list),grandparent_page,grandparent_click_list_num):
            print(f'意外回退到{enter_text_list}的爷爷界面')
            code = 4
            level = level -1
            print('level=', level)
            return code
        else:
            i = i + 1
            print(f'第{i}次尝试从{enter_text_list}返回父界面')
            driver.back()
            time.sleep(2)
    level = level - 1
    print('level=', level)
    code = 3
    return code


def initital():
    print('init_black_element...')
    init_black_element()


if __name__ == '__main__':

    initital()
    click_list_num = len(driver.find_elements(By.XPATH, './/*[@clickable = "true"]'))
    for i in range (click_list_num):
        if dfs_2(['初始化页面'],driver.page_source,click_list_num,'',0) !=5 :
            break
