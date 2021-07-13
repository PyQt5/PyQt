#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年2月24日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: IsSignalConnected
@description: 判断信号是否连接
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextBrowser


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.button1 = QPushButton('已连接', self, clicked=self.doTest)
        self.button2 = QPushButton('未连接', self)
        self.retView = QTextBrowser(self)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.retView)

    def doTest(self):
        self.retView.append("""
        # button1 clicked 是否连接: %s, %s
        # button2 clicked 是否连接: %s, %s
        """ % (
            self.isSignalConnected(self.button1, 'clicked()'),
            self.button1.receivers(self.button1.clicked) > 0,
            self.isSignalConnected(self.button2, 'clicked()'),
            self.button2.receivers(self.button2.clicked) > 0,
        ))

    def isSignalConnected(self, obj, name):
        """判断信号是否连接
        :param obj:        对象
        :param name:       信号名，如 clicked()
        """
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
