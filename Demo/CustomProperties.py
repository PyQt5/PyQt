#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年4月12日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: 自定义属性测试
@description: 
"""
from random import randint

try:
    from PyQt5.QtCore import pyqtProperty, pyqtSignal
    from PyQt5.QtWidgets import QPushButton, QApplication
except ImportError:
    from PySide2.QtCore import Property as pyqtProperty, Signal as pyqtSignal
    from PySide2.QtWidgets import QPushButton, QApplication


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

    app = QApplication(sys.argv)
    w = Window()
    w.setStyleSheet(
        "qproperty-textColor: white;qproperty-backgroundColor: red;")
    w.show()
    sys.exit(app.exec_())
