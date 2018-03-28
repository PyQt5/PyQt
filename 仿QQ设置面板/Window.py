#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from 仿QQ设置面板.SettingUi import Ui_Setting

# Created on 2018年3月28日
# author: Irony
# site: https://github.com/892768447
# email: 892768447@qq.com
# file: 仿QQ设置面板.Window
# description:

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class Window(QWidget, Ui_Setting):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.resize(877, 637)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(open("style.qss","rb").read().decode("utf-8"))
    w = Window()
    w.show()
    sys.exit(app.exec_())
