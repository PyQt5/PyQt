#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年4月12日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: 自定义属性测试
@description: 
'''
from random import randint

from PyQt5.QtCore import pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QPushButton


__version__ = "0.0.1"


class Window(QPushButton):

    bgChanged = pyqtSignal(str, str)

    def __init__(self):
        super(Window, self).__init__("QSS")
        self._textColor = ""
        self._backgroundColor = ""
        self.clicked.connect(self.onClick)
        self.bgChanged.connect(lambda old, new: print(
            "old bg color", old, "new bg color", new))

    def onClick(self):
        print("textColor", self._textColor)
        self.setStyleSheet("qproperty-backgroundColor: %s;" % randint(1, 1000))

    # 方式一、个人觉得比较简洁
    @pyqtProperty(str, notify=bgChanged)
    def backgroundColor(self):
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color):
        self.bgChanged.emit(self._backgroundColor, color)
        self._backgroundColor = color

    # 方式二
    def getTextColor(self):
        return self._textColor

    def setTextColor(self, c):
        self._textColor = c

    textColor = pyqtProperty(str, getTextColor, setTextColor)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.setStyleSheet(
        "qproperty-textColor: white;qproperty-backgroundColor: red;")
    w.show()
    sys.exit(app.exec_())
