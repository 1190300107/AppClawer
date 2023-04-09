# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
# @Time    : 2023/3/19 22:09
import time
from difflib import SequenceMatcher
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
import traceback

caps = {}
caps["platformName"] = "Android"
caps["ensureWebviewsHavePages"] = True
level = -1
MAX_LEVEL = 2
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
driver.implicitly_wait(3)

old_click_by_text_set=set()#根据按钮text记录当前元素是否遍历过，防止重复遍历
old_xml_set = set()
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


def is_black(element: webdriver.webelement.WebElement) -> bool:
    # print(element.get_attribute('content-desc'))
    try:
        content_desc = element.get_attribute('content-desc').lower()
        if content_desc in black_list_content_desc:
            print('content-desc',content_desc,'is black')
            return True
    except:
        pass
    try:
        text_list = parse_text_list(element)
        if text_list in black_element_by_parse_text:
            return True
    except:
        pass
    return False
def is_old(element: webdriver.webelement.WebElement)->bool:
    try:
        text_list = parse_text_list(element)
        if str(text_list) in old_click_by_text_set:
            return True
    except:
        pass
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


# def contain_white_text(element: webdriver.webelement.WebElement) -> bool:
#     """
#     判断element是否包含黑名单black_element_by_parse_text.txt之外的text
#     :param element:
#     :return:
#     """
#     text_list = parse_text_list(element)
#     if len(text_list) == 0 or text_list in black_element_by_parse_text:
#         return False
#
#     else:
#         return True


def parse_text_list(element: webdriver.webelement.WebElement):
    """
    提取元素中的所有text
    :param element:
    :return:
    """
    try:
        text_click_list = element.find_elements(By.XPATH, './/*[@text!=""]')
    except:
        print('提取text_list失败')
        text_click_list = []
        return text_click_list
    else:
        if len(text_click_list) == 0:
            return []
        else:
            text_list = [click.text for click in text_click_list]
            return text_list


def dif(str1, str2):
    print(SequenceMatcher(None, str1, str2).quick_ratio())
    return SequenceMatcher(None, str1, str2).quick_ratio()


def is_same(str1, str2):
    return dif(str1,str2) >0.98


# def search_try():
#     parent = driver.page_source
#     clickable_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')
#     # localtion =[]
#     # for item in clickable_list:
#     #     localtion.append([item.location['x'],item.location['y']])
#     for item in clickable_list:
#         print(item)
#         driver.implicitly_wait(1)
#         try:
#             item.click()
#         except:
#             print('元素丢失', item)
#             continue
#         # driver.save_screenshot(f'../picture/{}.png')
#
#         time.sleep(0.5)
#         while dif(driver.page_source, parent) < 0.95:
#             time.sleep(1)
#             # driver.save_screenshot(f'{local}.png')
#             print(dif(driver.page_source, parent), 'back')
#             driver.back()
#
#
# def search():
#     parent = driver.page_source
#     clickable_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')
#     localtion = []
#     for item in clickable_list:
#         localtion.append([item.location['x'], item.location['y']])
#     for local in localtion:
#         print(local)
#         TouchAction(driver).tap(x=local[0], y=local[1]).perform()
#         driver.save_screenshot(f'../picture/{local}.png')
#
#         time.sleep(0.5)
#         while dif(driver.page_source, parent) < 0.95:
#             time.sleep(1)
#             # driver.save_screenshot(f'{local}.png')
#             print(dif(driver.page_source, parent), 'back')
#             driver.back()
#
#
# # def dfs(parent_localtion_list:[]=[]):
# #     global level,MAX_LEVEL
# #
# #     level = level +1
# #     print('进入dfs level=',level)
# #     if level == MAX_LEVEL:
# #         print('达到最大深度,back')
# #         level = level -1
# #         return
# #     else:
# #         clickable_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')
# #         localtion = [[item.location['x'],item.location['y']] for item in clickable_list]
# #         localtion = [xy for xy in localtion if xy not in parent_localtion_list]#点击新出现的按钮。
# #         localtion = list(set(localtion))
# #         parent = driver.page_source
# #         for local in localtion[:20]:
# #             print(local)
# #             TouchAction(driver).tap(x=local[0], y=local[1]).perform()
# #
# #             time.sleep(0.5)
# #             if f(driver.page_source, parent) < 0.95:
# #                 driver.save_screenshot(f'../picture/{local}.png')
# #                 print(f(driver.page_source, parent),'forward')
# #                 dfs(localtion)
# #             else:
# #                 print('页面无变化')
# #         while f(driver.page_source, parent) < 0.95:
# #             time.sleep(1)
# #             # driver.save_screenshot(f'{local}.png')
# #             print(f(driver.page_source, parent), 'back')
# #             driver.back()
# #
# #         level = level -1
# #         return
def is_good_click(element: webdriver.webelement.WebElement):
    """
    遍历界面的element时候，判断element是否遍历过或者在黑名单那里
    :param element:
    :return:
    """
    text_list = parse_text_list(element)
    if not contain_text(element):
        print(text_list,'is empty! bad!')
        return False
    if is_old(element):
        print(text_list,'is old! bad!')
        return False
    if is_black(element):
        print(text_list,'is black! bad!')
        return False
    print(text_list,'is good! Just do it!')
    return True
def dfs_2(parent_page='',grandparent_page='') ->int:
    """
    深度优先搜索
    :param parent_page:父界面
    :return:
    0：到达最大层数
    1：当前界面已经访问过
    2：意外回到父界面，如点击了back按钮
    3：正常返回
    """
    global level
    global MAX_LEVEL
    global old_click_by_text_set
    level = level + 1
    print('\t' * level, 'level=', {level})
    code = 0
    if level == MAX_LEVEL:
        print('到达最大层数,返回')
        level = level - 1
        print('level=',level)
        return code
    current_page = driver.page_source
    if current_page in old_xml_set:
        print('当前界面已经访问过')
        level = level - 1
        print('level=', level)

        code=1
        return code
    else:
        old_xml_set.add(current_page)
        print('正在提取页面元素信息...')
        current_click_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')
        # current_click_list = [click for click in all_current_click_list if not is_old(click) if
        #                       not is_black(click) ]
        print('页面元素提取成功!')
        for click in current_click_list:
            if not is_good_click(click):
                continue
            text_list = parse_text_list(click)
            print('click on ', text_list)
            try:
                click.click()
            except:
                print(f'元素丢失', {click})
                continue
            else:
                old_click_by_text_set.add(str(text_list))
                time.sleep(1)
                new_page = driver.page_source
                if is_same(new_page, parent_page):
                    print('意外回退到父界面，将错就错，停止')
                    level = level - 1
                    code =2
                    return code
                elif is_same(new_page, grandparent_page):
                    print(f'意外回退到{text_list}的爷爷界面')
                    code = 4
                    level = level - 1
                    print('level=', level)
                    return code
                elif (dif(new_page, current_page) > 0.98):
                    current_page = new_page
                    print('点击无反应,忽略')
                else:
                    print('进入新界面', text_list)
                    code_child = dfs_2(current_page,parent_page)
                    if code_child ==4:#子界面遍历过程中意外跳转到爷爷界面,需要在父界面直接return，同时告知爷爷界面。
                        level = level -1
                        print('level=',level)
                        code =5
                        return code
                    if code_child ==5:
                        # current_click_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')#重新更新爷爷界面list，否则总丢失元素，不用担心重复遍历，因为有记录old_click_by_text_set
                        continue
                    if code_child==2:#子界面遍历的过程中意外跳转到父界面
                        # current_click_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')#重新更新父界面list，否则总丢失元素，不用担心重复遍历，因为有记录old_click_by_text_set
                        continue

                    for i in range(MAX_LEVEL * 2 + 1):
                        new_page = driver.page_source
                        if i == MAX_LEVEL * 2:
                            print('多次返回仍无法回到父界面,测试崩溃,将该界面入口元素标记为黑名单')
                            time.sleep(1)
                            with open('../config/black_element_by_parse_text.txt',encoding='utf8',mode='a+') as f:
                                f.write(str(text_list) + '\n')
                                exit(f'{text_list}被收录至black_element_by_parse_text.txt')
                        if is_same(new_page,grandparent_page):
                            print(f'意外回退到{text_list}的爷爷界面')
                            code = 4
                            level = level -1
                            print('level=', level)

                            return code
                        if not is_same(new_page, current_page):
                            i = i + 1

                            print(f'第{i}次尝试从{text_list}返回父界面')

                            driver.back()
                            time.sleep(3)
                        elif is_same(new_page,current_page):
                            print('返回成功')

                            current_page = new_page
                            break
                        else:
                            print('error')
                            exit('界面失控')

        level = level - 1
        print('level=', level)

        code = 3
        return code


def initital():
    print('init_black_element...')
    init_black_element()


if __name__ == '__main__':
    # dfs()
    # search_try()
    initital()
    dfs_2(driver.page_source)
