# -*- coding: utf-8 -*-
# @Author  : Wang Zhenghao
# @Email   : 289410265@qq.com
# @Time    : 2023/5/19 15:18
class Origin_exception(Exception):
    def __init__(self,enter_text:str):
        self.enter_text = enter_text