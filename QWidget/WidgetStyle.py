#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月10日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: test
@description: 
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout

from Lib.CustomPaintWidget import CustomPaintWidget  # @UnresolvedImport
from Lib.CustomWidget import CustomWidget  # @UnresolvedImport


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(CustomPaintWidget(self))
        layout.addWidget(CustomWidget(self))
        # 注意
        w = CustomWidget(self)
        w.setAttribute(Qt.WA_StyledBackground)  # 很重要
        layout.addWidget(w)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet('''
CustomPaintWidget {
    min-width: 100px;
    min-height: 100px;
    border: 1px solid green;
    border-radius: 20px;
    background: green;
}
CustomWidget {
    min-width: 200px;
    min-height: 200px;
    max-width: 200px;
    max-height: 200px;
    border: 1px solid orange;
    border-radius: 100px;
    background: orange;
}
    ''')
    w = Window()
    w.show()
    sys.exit(app.exec_())
