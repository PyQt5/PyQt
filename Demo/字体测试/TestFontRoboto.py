#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年3月30日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: TestFontRoboto
@description: 
'''

__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

import glob
import os
import sys

from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout


app = QApplication(sys.argv)

names = []

for path in glob.glob("Fonts/Roboto/*.ttf"):
    print("path", os.path.abspath(path))
    names.append(os.path.basename(path.replace(".ttf", "")).replace("-", ""))
    fid = QFontDatabase.addApplicationFont(os.path.abspath(path))
    print("fid", fid)
    print(QFontDatabase.applicationFontFamilies(fid))

w = QWidget()
w.setWindowTitle("Roboto Fonts")
layout = QGridLayout(w)

print("names", names)
for row in range(4):
    for col in range(4):
        layout.addWidget(QLabel(names[row * 4 + col],
                                font=QFont(names[row * 4 + col], 26)),
                         row, col, 1, 1)
#         print(row, col, row * 4 + col)

w.show()
sys.exit(app.exec_())
