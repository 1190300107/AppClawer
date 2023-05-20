# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
# @Time    : 2023/3/19 22:09
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

old_click_by_text_set=set()#根据按钮text记录当前元素是否遍历过，防止重复遍历
old_xml_set = set()
black_list_content_desc = ['back']
black_element_by_parse_text = []
black_element_by_resource_id=[]
origin_page =driver.page_source    #初始界面，即未打开app之前的界面
def init_black_element():
    """
    读取./config/black_element_by_parse_text.yaml，初始化按钮黑名单
    :return:
    """
    global black_element_by_parse_text
    global black_element_by_resource_id
    with open('../config/black_element_by_parse_text.yaml',encoding='utf8') as f:
        black_element_by_parse_text = yaml.load(f,yaml.FullLoader)
    print('black_element_by_parse_text:', black_element_by_parse_text)
    with open('../config/black_resource_id.yaml',encoding='utf8') as f:
        data  = yaml.load(f,Loader=yaml.FullLoader)
        black_element_by_resource_id = data
    print('black_element_by_resource_id:',black_element_by_resource_id)

def is_black(click) -> bool:

    # print(element.get_attribute('content-desc'))
    # try:
    #     content_desc = element.get_attribute('content-desc').lower()
    #     if content_desc in black_list_content_desc:
    #         print('content-desc',content_desc,'is black')
    #         return True
    # except:
    #     pass
    text = click['text']
    resource_id = click['resource-id']


    for black_text in black_element_by_parse_text:
        pattern = re.compile(black_text)
        flag = pattern.search(text)
        if flag:
            print(click,'text命中黑名单')
            return True
    for black_resourece_id in black_element_by_resource_id:
        if resource_id is not None:
            resource_id = resource_id[ resource_id.find('/'):]  # 去除前面的包名
            pattern = re.compile(black_resourece_id)
            flag = pattern.search(text)
            if flag:
                print(click, 'resource-id命中黑名单')
                return True
    return False
def is_old(click)->bool:
    text = click['text']
    if text in old_click_by_text_set:
        print(click,'is old! bad!')
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

def count_all_nodes(xml_string):
    root = ET.fromstring(xml_string)
    count = 0
    for elem in root.iter():
        count += 1
        count += len(elem.findall('.//*'))
    return count





# def parse_text_list(element: webdriver.webelement.WebElement):
#     """
#     提取元素中的所有text
#     :param element:
#     :return:
#     """
#     try:
#         # text_click_list = [element.find_element(By.XPATH, './/*[@text!=""]')]
#         text_click_list = [element.tag_name]
#     except Exception as e:
#         if 'Message: An element could not be located on the page using the given search param' in str(e):
#             print('元素不包含文字')
#             return []
#         else:
#             print('遇到新异常')
#             raise e
#     else:
#         if len(text_click_list) == 0:
#             return []
#         else:
#             text_list = []
#             for click in text_click_list:
#                 try:
#                     text = click.text
#                 except:
#                     continue
#                 else:
#                     text_list.append(text)
#             return text_list


def dif(str1, str2):
    print(SequenceMatcher(None, str1, str2).quick_ratio())
    return SequenceMatcher(None, str1, str2).quick_ratio()

def is_same(xml1,xml2):
    diff = main.diff_texts(xml1.encode(), xml2.encode())
    similarity = 1 - len(diff) / (count_all_nodes(xml1) + count_all_nodes(xml2))
    print('similarity:',similarity)
    return 1 - len(diff) / (count_all_nodes(xml1) + count_all_nodes(xml2))>0.95
# def is_same(str1,click_list_num1, str2,click_list_num2):
#     print('click_list_num1:',click_list_num1)
#     print('click_list_num2:',click_list_num2)
#     return dif(str1,str2) >0.95 and (abs(click_list_num1-click_list_num2) <=2 or click_list_num1 ==0 or click_list_num2 ==0 )

def is_good_click(click):
    """
    遍历界面的element时候，判断element是否遍历过或者在黑名单那里
    :param element:
    :return:
    """
    if is_old(click):
        return False
    elif is_black(click):
        return False
    else:
        print(click,'鉴定为好按钮，可以点击')
        return True
def search_element():
    """
    通过text!=""属性获取元素，后期根据坐标tap
    :return:
    """
    element_list = driver.find_elements(By.XPATH,'.//*[@text!=""]')
    return element_list
def judge_action_by_text_list(text:str):
    with open ('../config/action_keyword.yaml', encoding='utf8') as f:
        white_element_list = yaml.load(f,Loader=yaml.FullLoader)['action_list']
    for item in white_element_list:
        action = item.get('action')
        keyword_list = item.get('keyword_list')
        for keyword in keyword_list:
            try:
                pattern = re.compile(keyword)
                flag = pattern.search(text)
            except:
                print(keyword,'编译失败')
                traceback.print_exc()
            if flag:
                print(text, '命中规则:', keyword, '判定行为:', action)
                print(datetime.now())
                print(datetime.now().timestamp())
                return action
    # key_word = text_list[0]
    # regex_action_map = {}
    # regex_action_map[r'\d+$'] = '点击纯数字'
    # regex_action_map[r'赞$'] = '点赞'
    # regex_action_map[r'快转$'] = '快转'
    # regex_action_map[r'评论$'] = '评论'
    # regex_action_map[r'快送$'] = '快送'
    # for regex,action in regex_action_map.items():
    #     pattern = re.compile(regex)
    #     if pattern.match(key_word):
    #         print(key_word,'命中规则:',regex,'判定行为:',action)
    #         print(datetime.now())
    #         print(datetime.now().timestamp())
    #         return action
    return '未知行为'

def parse_info_from_click(clicklist:[webdriver.webelement.WebElement]):
    """
    为了防止回溯之后，按钮丢失，将element的上的text，location,resource-id记录下载，后续根据这个记录去遍历，而不是根据原始的element
    :param clicklist:
    :return:
    """
    myclick_list =[]
    for click in clicklist:
        try:
            text = click.text
            localtion = click.location

            if text in [added_click['text'] for added_click in myclick_list]:
                continue
            else:
                myclick = {'text':text,'location':localtion}
                try:
                    resource_id = click.get_attribute('resource-id')
                    myclick['resource-id'] = resource_id
                except:
                    print(text,'提取resource-id失败')
                myclick_list.append(myclick)

        except Exception as e:
            # print(text,'转换成自创的对象时失败')
            if """Message: Cached elements 'By.xpath: .//*[@text!=""]' do not exist in DOM anymore""" in str(e):
                print('元素寻找失败')
    return myclick_list
def log_click(click,time,timestamp):
    """
    记录点击日志
    :param click:
    :return:
    """
    text = click['text']
    action = judge_action_by_text_list(text)
    with open('../result/click_log.txt', 'a', encoding='utf-8') as f:
        result = f"{time}\t{click}\t{action}\t{timestamp}\n"
        print(result)
        f.write(result)
def update_element(click):
    """
    由于使用我自己创建的元素对象，所以回溯的时候更新这个元素
    判断是否还停留在界面上，比如直播的弹幕，回溯的时候可能会消失
    更新位置，比如点击回溯之后，因为历史记录的原因，导致原来的元素位置改变，返回新的位置

    :param click:
    :return:

    """
    new_location = {}
    parse_info_from_click_list = parse_info_from_click(search_element())
    parse_click_text =[click['text']  for click in parse_info_from_click_list]

    if  click['text'] not in parse_click_text:
        update_code =-1
    else:
        update_code =0
        index = parse_click_text.index(click['text'])
        new_location =parse_info_from_click_list[index]['location']
    return update_code,new_location

def dfs(enter_text,parent_page,grandparent_page) ->int:
    """

    :param enter_text:当前界面入口
    :param parent_page:当前界面的父界面
    :param grandparent_page:当前界面的爷爷界面
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
    global origin_page
    driver.implicitly_wait(3)

    level = level + 1
    print('\t' * level, 'level=', {level})

    if level == MAX_LEVEL:
        print('到达最大层数,返回')
        for i in range(MAX_LEVEL * 2 +1):
            new_page = driver.page_source
            if i == MAX_LEVEL * 2:
                print('多次返回仍无法回到父界面,测试崩溃,将该界面入口元素标记为黑名单')
                with open('../config/black_element_by_parse_text.yaml', encoding='utf8', mode='a+') as f:
                    # f.write(str([enter_text]) + '\n')
                    # exit(f'{enter_text}被收录至black_element_by_parse_text.txt')
                    yaml.dump([enter_text],f,encoding='utf8',allow_unicode=True)
                    raise Origin_exception(enter_text)
            elif is_same(new_page, origin_page):
                print('回退到桌面，抛出异常，重新开始')
                raise Origin_exception(enter_text)
            elif is_same(new_page, parent_page):
                print('返回父界面成功')
                break
            elif is_same(new_page,  grandparent_page):
                print(f'意外回退到{enter_text}的爷爷界面')
                code = 4
                level = level - 1
                print('level=', level)
                return code
            else:
                i = i + 1
                print(f'第{i}次尝试从{enter_text}返回父界面')
                driver.back()
                Time.sleep(2)
        level = level - 1
        print('level=',level)
        code = 0
        return code
    else:#未达到最大层数，开始提取元素，遍历界面
        current_page = driver.page_source
        print('正在提取页面元素信息...')
        current_click_list = parse_info_from_click(search_element())
        print(current_click_list)
        print('页面元素提取成功!')

        for i,click in enumerate (current_click_list):
            print('正在遍历',enter_text,'界面的第',i+1,'个按钮',click['text'])
            update_code,new_location = update_element(click)
            if update_code ==-1:
                print(click['text'],'不存在于',enter_text,'界面,不再继续遍历')
                continue
            else:
                print(click['text'],'存在于',enter_text,'界面，继续遍历')

                text = click['text']
                print('当前按钮文字',text)
                if not is_good_click(click):
                    continue
                print('click on ', text)
                try:
                    time_start = datetime.now()
                    timestamp_start = datetime.now().timestamp()
                    TouchAction(driver).tap(x=new_location['x']+1,y=new_location['y']+1).perform()

                except:
                    print(f'元素丢失', {text})
                    continue
                else:
                    action = judge_action_by_text_list(text)
                    if action == '未知行为':
                        print(text,'是未知行为，添加到旧名单当中')
                        old_click_by_text_set.add(text)
                    else:
                        print(text, '是',action,'行为','无需添加到旧名单')
                    Time.sleep(2)
                    new_page = driver.page_source
                    if (dif(new_page, current_page) > 0.98):
                        current_page = new_page
                        print('点击无反应,忽略')
                        continue
                    elif is_same(new_page,origin_page):
                        print('回退到桌面，抛出异常，重新开始')
                        raise Origin_exception(enter_text)
                    elif is_same(new_page,parent_page):
                        print('意外回退到父界面，将错就错，停止')
                        level = level - 1
                        code =2
                        return code
                    elif is_same(new_page,  grandparent_page):
                        print(f'意外回退到{text}的爷爷界面')
                        code = 4
                        level = level - 1
                        print('level=', level)
                        return code
                    else:
                        print('进入新界面', text)
                        log_click(click,time_start,timestamp_start)
                        Time.sleep(3)
                        code_child = dfs(text,current_page,parent_page)#子dfs返回时，已经保证回退到进入dfs之前click之前的页面（即current_page），或者parent_page
                        if code_child ==4:#子界面遍历过程中意外跳转到爷爷界面,需要在此界面直接return，同时告知爷爷界面。
                            level = level -1
                            print('level=',level)
                            code =5
                            return code
                        elif code_child ==5:
                            print('孙子界面意外跳转到本爷爷界面==',enter_text)
                            current_click_list.append(click)#将孙子界面的父界面入口重新添加到队列尾部
                            if text in old_click_by_text_set:
                                old_click_by_text_set.remove(text)#孙子界面的父界面入口从旧名单中除去
                            continue
                        elif code_child==2:#子界面遍历的过程中意外跳转到父界面(即当前current_page)
                            # current_click_list = driver.find_elements(By.XPATH, './/*[@clickable = "true"]')#重新更新父界面list，否则总丢失元素，不用担心重复遍历，因为有记录old_click_by_text_set
                            print('儿子界面意外跳转到本父亲界面==',enter_text)
                            continue
                        elif code_child ==0:
                            print('儿子界面达到最大层数，正常返回到本父亲界面==',enter_text)
                        elif code_child ==3:
                            print('儿子界面所有文字按钮已经遍历完毕，正常返回本父亲界面==',enter_text)

        print('当前界面==',enter_text,'所有文字按钮已经遍历完毕')
    for i in range(MAX_LEVEL * 2 +1):
        new_page = driver.page_source
        Time.sleep(2)
        if i == MAX_LEVEL * 2:
            print('多次返回仍无法回到父界面,测试崩溃,将该界面入口元素标记为黑名单')
            Time.sleep(2)
            with open('../config/black_element_by_parse_text.yaml',encoding='utf8',mode='a+') as f:
                # f.write(str([enter_text]) + '\n')
                # exit(f'{enter_text}被收录至black_element_by_parse_text.txt')
                yaml.dump([enter_text], f, encoding='utf8', allow_unicode=True)
                raise  Origin_exception(enter_text)
        elif is_same(new_page, origin_page):
            print('回退到桌面，抛出异常，重新开始')
            raise Origin_exception(enter_text)
        elif is_same(new_page, parent_page):
            print('返回父界面成功')
            break

        elif is_same(new_page,grandparent_page):
            print(f'意外回退到{enter_text}的爷爷界面')
            code = 4
            level = level -1
            print('level=', level)
            return code
        else:
            i = i + 1
            print(f'第{i}次尝试从{enter_text}返回父界面')
            driver.back()
            Time.sleep(2)
    level = level - 1
    print('level=', level)
    code = 3
    return code


def initital():
    print('init_black_element...')
    init_black_element()
def start_fritap(app_name,pcap_dump_path='../pcap'):
    """
    使用fritap进行捕包，awk8是模拟器，awk9是真机
    :param app_name:
    :param pcap_dump_path:
    :return:
    """
    cmd_find_app_id_process_name = "adb shell ps -d | grep %s | awk '{print $2,$8}'" %(app_name)
    print(cmd_find_app_id_process_name)
    child = subprocess.run(cmd_find_app_id_process_name,stdout=subprocess.PIPE)
    if len(child.stdout) ==0:
        print('定位pid失败')
        raise
    else:
        for line in child.stdout.decode().split('\r\n')[:-1]:
            print(line)
            app_pid  = eval(line.split(' ')[0])
            process_name =line.split(' ')[1].replace('\r\n','').replace(':','-')
            print(app_pid)
            print(process_name)
            cmd_start_fritap = f'python ../../../lib/friTap-main/friTap.py -m {app_pid} -p {pcap_dump_path}/{process_name}-{app_pid}-{datetime.now().timestamp()}-fritap.pcap'
            print(cmd_start_fritap)
            subprocess.Popen(cmd_start_fritap, shell=True)
def start_tcpdump(app_name:str):
    cmd_find_app_port = "adb shell netstat -tunep | grep %s | awk '{print $4}'"%(app_name)
    print(cmd_find_app_port)
    child = subprocess.run(cmd_find_app_port,stdout=subprocess.PIPE)
    if len(child.stdout) ==0:
        print('定位pid失败')
        raise
    else:
        port_list =[]
        for line in child.stdout.decode().split('\r\n')[:-1]:
            print(line)
            port = line.split(' ')[0].split(':')[-1]
            print(port)
            port_list.append(port)
        port_str = ' or '.join(port_list)
        cmd_start_tcpdump = 'adb shell tcpdump port '+port_str+f' -w /data/local/tmp/{app_name}-{datetime.now().timestamp()}-tcpdump.pcap'
        print(cmd_start_tcpdump)
        subprocess.Popen(cmd_start_tcpdump,shell=True)
if __name__ == '__main__':

    initital()
    while True:
        app_package = input('请输入app包名:')
        app_activity = input('请输入app活动名')
        print('正在启动app')
        cmd_start_app = f'adb shell am start -n {app_package}/{app_activity}'
        print(cmd_start_app)
        child = subprocess.run(cmd_start_app, stderr=subprocess.PIPE)
        Time.sleep(2)
        if 'Error' in child.stderr.decode():
            print(child.stderr.decode())
            print('app启动失败,请输入正确的app包名和app活动名')
            continue
        else:
            start_fritap(app_name=app_package)
            start_tcpdump(app_name=app_package)
            break
    while True:
        try:
            dfs(['初始化页面'],origin_page,origin_page)
        except Origin_exception:
            print('正在杀死app')
            cmd_kill_app = "adb shell ps -d | grep %s |  awk '{print $3}'"%(app_package)
            print(cmd_kill_app)
            child = subprocess.run(cmd_kill_app,stdout=subprocess.PIPE)
            for pid in child.stdout.decode().split('\r\n')[:-1]:
                cmd_kill_pid = f"adb shell kill {pid}"
                print(cmd_kill_pid)
                subprocess.run(cmd_kill_pid)
            Time.sleep(10)
            print('正在重新启动app')
            cmd_start_app = f'adb shell am start -n {app_package}/{app_activity}'
            child = subprocess.run(cmd_start_app, stdout=subprocess.PIPE)
            Time.sleep(10)
            level = -1
            start_fritap(app_name=app_package)
            start_tcpdump(app_name=app_package)
            print('正在重新建立连接')
            driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
            Time.sleep(10)
            origin_page = driver.page_source

            continue
        else:
            break

