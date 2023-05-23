# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
# @Time    : 2023/5/22 22:07
import subprocess
if __name__ == '__main__':
    cmd = 'python start.py'
    for i in range(3):
        print(i)
        child=subprocess.run(cmd)

        print(i)