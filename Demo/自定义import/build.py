#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月28日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: build
@description: 
'''

__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"
import base64

import xxtea  # @UnresolvedImport


KEY = base64.b85decode("HF5^hbNbOVOKM=(SB`7h")

with open("src/test.py", "rb") as fi:
    open("test.irony", "wb").write(xxtea.encrypt(fi.read(), KEY))
print("ok")
