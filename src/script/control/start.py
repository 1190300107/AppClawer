# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
# @Time    : 2023/5/22 11:09
import os
import sys
from datetime import datetime
import subprocess
import time
import scapy.all
import yaml
from scapy.all import *
from appium import webdriver
import signal


from src.script.script_code import weibo_hotnews, weibo_like, cntvnews_news


global caps
global driver
def initialize():
    global caps
    global driver
    caps = {}
    caps["platformName"] = "Android"
    caps["devicesName"] = '127.0.0.1：62025'
    caps["appPackage"] = 'com.sina.weibo'
    caps ["appActivity"] = '.MainTabActivity'
    caps["ensureWebviewsHavePages"] = True

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)

def start_fritap(app_name,pcap_dump_path='../pcap'):
    """
    使用fritap进行捕包，awk8是模拟器，awk9是真机
    :param app_name:
    :param pcap_dump_path:
    :return:
    """
    cmd_find_app_id_process_name = "adb shell su -c ps -d | grep %s | awk '{print $2,$9}'" %(app_name)
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
            child = subprocess.Popen(cmd_start_fritap, shell=True)
            return child
def start_tcpdump(app_name:str):
    cmd_find_app_port = "adb shell su -c  netstat -tunep | grep %s | awk '{print $4}'"%(app_name)
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
        dump_file = f'{app_name}-{datetime.now().timestamp()}-tcpdump.pcap'
        cmd_start_tcpdump = 'adb shell su -c  tcpdump port '+port_str+f' -w /data/local/tmp/{dump_file}'
        print(cmd_start_tcpdump)
        child = subprocess.Popen(cmd_start_tcpdump,shell=True)
        return dump_file,child
def stop_tcpdump():
    cmd_kill_tcpdump = "adb shell su -c ps -A | grep tcpdump |  awk '{print $2}'"
    print(cmd_kill_tcpdump)
    child = subprocess.run(cmd_kill_tcpdump, stdout=subprocess.PIPE)
    for pid in set(child.stdout.decode().split('\r\n')[:-1]):
        cmd_kill_pid = f"adb shell su -c kill {pid}"
        print(cmd_kill_pid)
        subprocess.run(cmd_kill_pid)
def copy_pcap(dump_file,dst_path='../pcap'):
    """
    从安卓手机中把tcpdump的pcap流量复制到windows中
    :return:
    """
    cmd_pull = f"adb pull /data/local/tmp/{dump_file} {dst_path}"
    print(cmd_pull)
    subprocess.run(cmd_pull)


def read_pcap(pcap_path: os.path):
    """
    读取总pcap包
    :param pcap_path:
    :return:
    """
    print('正在读取pcpa包...', pcap_path)
    pkts = rdpcap(pcap_path)
    print('读取成功!')
    return pkts

def read_click_log(log_file: str):
    with open(log_file, encoding='utf8') as f:
        data  = yaml.load(f,Loader=yaml.FullLoader)
    return data

def packet_filter(packet: scapy.all.Packet, timestamp_start):
    time_gap = 5
    timestamp_start = float(timestamp_start)
    timestamp_end = timestamp_start + int(time_gap)
    return packet.time > timestamp_start and packet.time < timestamp_end

def tag_pcap(timestamp: Decimal, pkts: scapy.all.PacketList, pcap_name: str):
    """
    根据时间戳和总包，筛选出时间戳之后数秒的包，并命名为pcap_name
    :param timestamp: 时间戳
    :param pkts: 总包
    :param pcap_name:新建的包
    :return:
    """
    print('正在根据', timestamp, '标记数据包', '将命名为', pcap_name)
    pacp_list = [p for p in pkts if packet_filter(p, timestamp)]
    count = len(pacp_list)
    print('总共过滤出包数量:', count)
    if count == 0:
        print('包个数为0,创建失败')
        return None
    else:
        wrpcap(pcap_name, pacp_list)
        print('创建pcap成功')






def tag(src_path='../pcap',dst_path='../taged_pcap'):



    click_log_file = r'../data/click_log.yaml'
    click_log_list = read_click_log(click_log_file)
    pcap_dir = src_path
    pcap_list = os.listdir(pcap_dir)
    for pcap in pcap_list:
        pcap_file = os.path.join(pcap_dir,pcap)
        packet_list = read_pcap(pcap_file)
        for click_log in click_log_list:
            timestamp = click_log['timestamp']
            action =  click_log['action']
            creat_pcap_file = os.path.join(dst_path,action+'-'+pcap)
            tag_pcap(timestamp,packet_list,creat_pcap_file)

if __name__ == '__main__':
    for i in range(2):
        print('start...')

        p1 = cntvnews_news.connect()
        p1.start()
        child_fritap=start_fritap(app_name=p1.get_package())

        dump_file,child_tcpdump = start_tcpdump(app_name=p1.get_package())
        p1.action()
        stop_tcpdump()
        time.sleep(3)
        copy_pcap(dump_file)
    tag()

    # initialize()
    # while True:
    #     # app_package = input('请输入app包名:')
    #     # app_activity = input('请输入app活动名:')
    #     app_package = 'com.sina.weibo'
    #     app_activity = '.MainTabActivity'
    #     print('正在启动app')
    #     cmd_start_app = f'adb shell am start -n {app_package}/{app_activity}'
    #     print(cmd_start_app)
    #     child = subprocess.run(cmd_start_app, stderr=subprocess.PIPE)
    #
    #     if 'Error' in child.stderr.decode():
    #         print(child.stderr.decode())
    #         print('app启动失败,请输入正确的app包名和app活动名')
    #         continue
    #     else:
    #         for i in range(5):
    #             start_fritap(app_name=app_package)
    #             # start_tcpdump(app_name=app_package)
    #         # p1 = weibo_hotnews.connect(driver)
    #         #
    #         # p1.start()
    #         #     time.sleep(15)
    #             initialize()
    #             p2 = weibo_hotnews.connect(driver)
    #             p2.start()
    #             # stop(app_package)
    #             cmd_start_app = f'adb shell am start -n {app_package}/{app_activity}'
    #             print(cmd_start_app)
    #             child = subprocess.run(cmd_start_app, stderr=subprocess.PIPE)
