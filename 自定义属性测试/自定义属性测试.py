#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年4月12日
@author: Irony."[讽刺]
@site: alyl.vip, orzorz.vip, irony.coding.me , irony.iask.in , mzone.iask.in
@email: 892768447@qq.com
@file: 自定义属性测试
@description: 
'''
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtProperty

__version__ = "0.0.1"

class Window(QPushButton):
    
    def __init__(self):
        super(Window, self).__init__("QSS")
        self._textColor = ""
        self.clicked.connect(lambda:print(self._textColor))
    
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
    w.setStyleSheet("qproperty-textColor: white;")
    w.show()
    sys.exit(app.exec_())
