#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年1月28日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: build
@description: 
"""

import base64

import xxtea  # @UnresolvedImport

KEY = base64.b85decode("HF5^hbNbOVOKM=(SB`7h")

with open("src/test.py", "rb") as fi:
    open("test.irony", "wb").write(xxtea.encrypt(fi.read(), KEY))
print("ok")
