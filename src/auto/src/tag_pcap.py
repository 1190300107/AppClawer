# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
# @Time    : 2023/4/15 19:37
#用于根据click_log.txt和总pcap包，标记出各个点击的流量
import os

import scapy.all
from scapy.all import *
class Click_log:
    def __init__(self,log_tuple:str):
        time = log_tuple.split('\t')[0]
        click = log_tuple.split('\t')[1]
        action = log_tuple.split('\t')[2]
        timestamp = log_tuple.split('\t')[3].strip('\n')
        self.time = time
        self.click =eval(click)
        self.action = action
        self.timestamp = timestamp
    def create_pcap_name(self):
        pcap_name = '-'.join([self.action,self.timestamp])+'.pcap'
        return pcap_name


def read_pcap(pcap_path:os.path):
    """
    读取总pcap包
    :param pcap_path:
    :return:
    """
    print('正在读取pcpa包...',pcap_path)
    pkts = rdpcap(pcap_path)
    print('读取成功!')
    return pkts
def packet_filter(packet:scapy.all.Packet,timestamp_start):
    time_gap = 5
    timestamp_start = float(timestamp_start.strip('\n'))
    timestamp_end =timestamp_start+int(time_gap)
    return packet.time > timestamp_start and packet.time < timestamp_end

def tag_pcap(timestamp:Decimal,pkts:scapy.all.PacketList,pcap_name:str):
    """
    根据时间戳和总包，筛选出时间戳之后数秒的包，并命名为pcap_name
    :param timestamp: 时间戳
    :param pkts: 总包
    :param pcap_name:新建的包
    :return:
    """
    print('正在根据',timestamp,'标记数据包','将命名为',pcap_name)
    pacp_list = [p for p in pkts if packet_filter(p,timestamp)]
    count  =len(pacp_list)
    print('总共过滤出包数量:',count)
    if count ==0:
        print('包个数为0,创建失败')
        return None
    else:
        # for p in pacp_list:
        #     print(p.summary())

        wrpcap(pcap_name,pacp_list)
        print('创建pcap成功')
def read_click_log(log_file:str):
    with open(log_file,encoding='utf8') as f:
        log_tuples=f.readlines()
    click_log_list = []
    for log in log_tuples:
        click_log = Click_log(log)
        click_log_list.append(click_log)
    return click_log_list
if __name__ == '__main__':
    click_log_file = r'../result/click_log.txt'
    click_log_list = read_click_log(click_log_file)
    pcap_file = '../pcap/cn.pcap'
    packet_list = read_pcap(pcap_file)
    for click_log in click_log_list:
        timestamp = click_log.timestamp
        creat_pcap_file = os.path.join(r'../taged_pcap',click_log.create_pcap_name())
        tag_pcap(timestamp,packet_list,creat_pcap_file)