# -*- coding: utf-8 -*-
'''
读取CSS用模块。
'''
class CommonHelper :

    def __init__(self ) :
        pass
         
    @staticmethod    
    def readQss( style):
        with open( style , 'r') as f:
           return f.read()

