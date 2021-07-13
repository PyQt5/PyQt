#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月23日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ShowFrameWhenDrag
@description: 调整窗口显示边框
"""
from ctypes import sizeof, windll, c_int, byref, c_long, c_void_p, c_ulong, c_longlong, \
    c_ulonglong, WINFUNCTYPE, c_uint

try:
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
except ImportError:
    from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication

if sizeof(c_long) == sizeof(c_void_p):
    WPARAM = c_ulong
    LPARAM = c_long
elif sizeof(c_longlong) == sizeof(c_void_p):
    WPARAM = c_ulonglong
    LPARAM = c_longlong

WM_NCLBUTTONDOWN = 0x00a1
GWL_WNDPROC = -4
SPI_GETDRAGFULLWINDOWS = 38
SPI_SETDRAGFULLWINDOWS = 37
WNDPROC = WINFUNCTYPE(c_long, c_void_p, c_uint, WPARAM, LPARAM)

try:
    CallWindowProc = windll.user32.CallWindowProcW
    SetWindowLong = windll.user32.SetWindowLongW
    SystemParametersInfo = windll.user32.SystemParametersInfoW
except:
    CallWindowProc = windll.user32.CallWindowProcA
    SetWindowLong = windll.user32.SetWindowLongA
    SystemParametersInfo = windll.user32.SystemParametersInfoA


def GetDragFullwindows():
    rv = c_int()
    SystemParametersInfo(SPI_GETDRAGFULLWINDOWS, 0, byref(rv), 0)
    return rv.value


def SetDragFullwindows(value):
    SystemParametersInfo(SPI_SETDRAGFULLWINDOWS, value, 0, 0)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('拖动或者调整窗口试试看'))

        # 重点替换窗口处理过程
        self._newwndproc = WNDPROC(self._wndproc)
        self._oldwndproc = SetWindowLong(
            int(self.winId()), GWL_WNDPROC, self._newwndproc)

    def _wndproc(self, hwnd, msg, wparam, lparam):
        if msg == WM_NCLBUTTONDOWN:
            # 获取系统本身是否已经开启
            isDragFullWindow = GetDragFullwindows()
            if isDragFullWindow != 0:
                # 开启虚线框
                SetDragFullwindows(0)
                # 系统本身处理
                ret = CallWindowProc(
                    self._oldwndproc, hwnd, msg, wparam, lparam)
                # 关闭虚线框
                SetDragFullwindows(1)
                return ret
        return CallWindowProc(self._oldwndproc, hwnd, msg, wparam, lparam)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
