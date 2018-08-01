#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 2018年8月2日
# author: Irony
# site: https://github.com/892768447
# email: 892768447@qq.com
# file: win无边框调整大小
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


import ctypes.wintypes

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import win32api
import win32con
import win32gui


class Window(QWidget):

    BorderWidth = 5

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setWindowFlags(Qt.Window
                            | Qt.FramelessWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint
                            | Qt.WindowCloseButtonHint)
        # 增加薄边框
        style = win32gui.GetWindowLong(int(self.winId()), win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            int(self.winId()), win32con.GWL_STYLE, style | win32con.WS_THICKFRAME)

    def nativeEvent(self, eventType, message):
        retval, result = super(Window, self).nativeEvent(eventType, message)
        if eventType == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            if msg.message == win32con.WM_NCCALCSIZE:
                # 拦截不显示顶部的系统自带的边框
                return True, 0
            if msg.message == win32con.WM_NCHITTEST:
                # 获取鼠标移动经过时的坐标
                x = win32api.LOWORD(msg.lParam) - self.frameGeometry().x()
                y = win32api.HIWORD(msg.lParam) - self.frameGeometry().y()
                w, h = self.width(), self.height()
                lx = x < self.BorderWidth
                rx = x > w - self.BorderWidth
                ty = y < self.BorderWidth
                by = y > h - self.BorderWidth
                # 左上角
                if (lx and ty):
                    return True, win32con.HTTOPLEFT
                # 右下角
                if (rx and by):
                    return True, win32con.HTBOTTOMRIGHT
                # 右上角
                if (rx and ty):
                    return True, win32con.HTTOPRIGHT
                # 左下角
                if (lx and by):
                    return True, win32con.HTBOTTOMLEFT
                # 上
                if ty:
                    return True, win32con.HTTOP
                # 下
                if by:
                    return True, win32con.HTBOTTOM
                # 左
                if lx:
                    return True, win32con.HTLEFT
                # 右
                if rx:
                    return True, win32con.HTRIGHT
                # 标题
                return True, win32con.HTCAPTION
        return retval, result


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
