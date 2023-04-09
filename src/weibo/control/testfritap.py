# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
# @Time    : 2023/2/28 10:29
import os
import re
import signal
import subprocess
import time


def cmd():
    app = 'com.sina.weibo'
    action = 'hotnews.py'
    cmd_fserver='adb shell su -c /data/local/tmp/fserver'
    cmd_fritap = f'C:\\myfile\design\\frida\\fritap\\friTap-main\\friTap.py'
    print(cmd_fserver,sep='\n')
    p_server = subprocess.Popen(cmd_fserver,shell=True)

    print(cmd_fritap)
    p_fritap = subprocess.Popen(['python',cmd_fritap,'-m','com.sina.weibo','-p','C:\myfile\design\mycode\src\weibo\pcap\hotnews.py.pcap','--spawn'])
    time.sleep(5)
    p_fritap.kill()
    # cmd1='adb shell ps -u root |findstr fserver '
    # ps=os.popen(cmd1)
    # line=ps.read()
    # pid=re.search('\d+',line).group()
    # cmd2=f'adb shell su -c kill {pid}'
    # os.system(cmd2)
    # print(cmd2)
def tr():
    # p = subprocess.Popen(['python','../../../main.py'])
    os.popen('start python ../script/hotnews.py')
    print(123123123)
    time.sleep(4)

if __name__ == '__main__':
    # cmd()
    tr()