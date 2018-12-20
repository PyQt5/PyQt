#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年12月6日
@author: Irony
@site: https://pyqt5.com, https://github.com/892768447
@email: 892768447@qq.com
@file: 
@description: 
"""

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0

import sys

from PyQt5.QtWidgets import QApplication

from CopyContent import TableView


app = QApplication(sys.argv)
app.setApplicationName("TableView")
w = TableView()
w.show()
sys.exit(app.exec_())