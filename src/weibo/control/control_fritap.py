# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
# @Time    : 2022/12/6 16:25
import os
import re
import subprocess
import sys
import threading
import time

from addcode import *
filelist=[]
def getfile()->list:
    global filelist
    filelist=os.listdir(r'../script')
    filelist.remove('__init__.py')
    for i in range(len(filelist)):
        filelist[i]= os.path.join('../script',filelist[i])
    return filelist
def initdir():#创建文件夹
    cmd='adb shell mkdir /data/local/tmp/weibo;'
    os.system(cmd)
    print(cmd)
def startfserver():#开启fridaserver
    cmd=f'adb shell su -c /data/local/tmp/fserver'
    print(cmd)
    sys.Popen(cmd)
# def startfritap(app:str,action:str,time=1):#开启fritap
#     cmd_fritap = f'python C:\\myfile\design\\frida\\fritap\\friTap-main\\friTap.py -m {app} -p ../pcap/{action+str(i)}.pcap --spawn'
#     print(cmd_fritap)
#     os.system(cmd_fritap)
# def closEcap():#关闭fserver,同时fritap也会自动退出
#     cmd1='adb shell ps -u root |findstr fserver '
#     ps=os.popen(cmd1)
#     line=ps.read()
#     pid=re.search('\d+',line).group()
#     cmd2=f'adb shell su -c  kill {pid}'
#     print(cmd2)
#     os.system(cmd2)
if __name__ == '__main__':
    filelist = getfile()
    print(filelist)
    addsleep(filelist)
    addimporttouch(filelist)
    initdir()
    print('startfserver...')
    os.popen('adb shell su -c /data/local/tmp/fserver')
    for file in filelist:

        creatfile = re.search(r'\\(\w+)\.?',file).group(1)
        cmd= fr'python {file}'
        for i in range(2):
            print(i, cmd)

            print('startfritap...')

            cmd_fritap = f'C:\\myfile\design\\frida\\fritap\\friTap-main\\friTap.py'

            p_fritap = subprocess.Popen(['python', cmd_fritap, '-m', 'com.sina.weibo', '-p',f'C:\myfile\design\mycode\src\weibo\pcap\{creatfile}'+str(i)+'.pcap', '--spawn'])
            # time.sleep(5)
            # p_fritap.communicate()
            # print(2)
            # os.system('tasklist')

            # time.sleep(5)
            os.system(cmd)
            # time.sleep(2)
            # p_action= subprocess.Popen(cmd)
            # p_action.wait()
            # subprocess.call(['python',{file}])
            # time.sleep(5)
            print('closefritap...')
            p_fritap.kill()
            time.sleep(3)


