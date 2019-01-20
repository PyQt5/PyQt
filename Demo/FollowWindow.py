#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月22日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: FollowWindow
@description: 跟随外部窗口
"""
import os

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
import win32gui


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton('test', self))
        self.tmpHwnd = None
        # 启动定时器检测记事本的位置大小和是否关闭
        self.checkTimer = QTimer(self, timeout=self.checkWindow)
        self.checkTimer.start(10)  # 10毫秒比较流畅

    def checkWindow(self):
        # 查找
        hwnd = win32gui.FindWindow('Notepad', None)
        if self.tmpHwnd and not hwnd:
            # 表示记事本关闭了
            self.checkTimer.stop()
            self.close()  # 关闭自己
            return
        if not hwnd:
            return
        self.tmpHwnd = hwnd
        # 获取位置
        rect = win32gui.GetWindowRect(hwnd)
        print(rect)
        self.move(rect[2], rect[1])


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    # 先检测是否已有记事本打开
    hwnd = win32gui.FindWindow('Notepad', None)
    print('hwnd', hwnd)
    if not hwnd:
        # 启动记事本
        os.startfile('notepad')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
