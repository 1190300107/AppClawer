# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
# @Time    : 2022/12/6 16:25
import os
import re
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
def startEcap(actionname:str,time=1):#开启ecapture

    cmd=f'adb shell cd /data/local/tmp/weibo;../ecapture tls -i eth0 -w /data/local/tmp/weibo/{actionname}{time}.pcapng'
    print(cmd)
    os.system(cmd)
def closEcap():#关闭ecapture
    cmd1='adb shell ps |findstr ecapture '
    ps=os.popen(cmd1)
    line=ps.read()
    pid=re.search('\d+',line).group()
    cmd2=f'adb shell kill {pid}'
    os.system(cmd2)
    print(cmd2)
if __name__ == '__main__':
    filelist = getfile()
    print(filelist)
    addsleep(filelist)
    addimporttouch(filelist)
    initdir()
    for file in filelist:
        creatfile = re.search(r'\\(\w+)\.?',file).group(1)

        cmd= fr'python {file}'
        for i in range(50):
            print(i, cmd)

            thread1 = threading.Thread(name='t1', target=startEcap, args=(creatfile,i))
            thread1.start()
            os.system(cmd)

            thread2 = threading.Thread(name='t2', target=closEcap)
            thread2.start()
            time.sleep(3)


