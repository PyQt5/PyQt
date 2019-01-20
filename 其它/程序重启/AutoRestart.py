#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年3月31日
@author: Irony."[讽刺]
@site: https://pyqt5.com, https://github.com/892768447
@email: 892768447@qq.com
@file: AutoRestart
@description: 
'''

from optparse import OptionParser
import os
import sys
import time


def restart(twice):
    os.execl(sys.executable, sys.executable, *[sys.argv[0], "-t", twice])

if __name__ == "__main__":
    parser = OptionParser(usage="usage:%prog [optinos] filepath")
    parser.add_option("-t", "--twice", type="int", dest="twice", default=1, help="运行次数")
    options, _ = parser.parse_args()
    print("app start...%s...twice\n" % options.twice)
    print("app pid: ",os.getpid())
    print("3秒后自动重启...\n")
    time.sleep(3)
    restart(str(options.twice + 1))
