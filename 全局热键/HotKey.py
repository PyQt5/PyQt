#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月11日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: HotKey
@description: 
'''
import ctypes  # @UnusedImport
import ctypes.wintypes
from datetime import datetime
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout,\
    QMessageBox, QTextBrowser, QPushButton


# 参考
# https://github.com/wujunwei/python-cookbook/blob/6e550d1a2b2b045cb07e56dd0198ccf01a2f3ea1/HotKey.py
# https://github.com/chenyijie4238215/notebook/blob/ba11fcc43cf8d623d1d1a722c261ddc20ad6b941/global_hotkey/GlobalHotKey.py
__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

WM_HOTKEY = 0x0312
MOD_ALT = 0x0001
MOD_NONE = 0x000
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008

Modifier = {
    "None": MOD_NONE,
    "Ctrl": MOD_CONTROL,
    "Alt": MOD_ALT,
    "Shift": MOD_SHIFT,
    "Win": MOD_WIN
}


class Window(QWidget):

    KeyIds = {}

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.logView = QTextBrowser(self)
        self.logView.append("点击右上角关闭按钮会隐藏窗口,通过热键Alt+S来显示")
        self.logView.append("等待热键中")
        layout.addWidget(QPushButton("退出整个程序", self, clicked=self.onQuit))
        layout.addWidget(self.logView)

    def unregisterHotKey(self, kid):
        ctypes.windll.user32.UnregisterHotKey(ctypes.c_int(self.winId()), kid)

    def registerHotKey(self, kid, modifier, key):
        key = str(key).upper()
        _modifier = Modifier.get(modifier, None)
        if not _modifier:
            return QMessageBox.critical(self, "错误", "modifier key {0}未找到".format(modifier))
        success = ctypes.windll.user32.RegisterHotKey(
            ctypes.c_int(self.winId()), kid, _modifier, ord(key))
        if success:
            self.KeyIds[kid] = modifier + "+" + key
            self.logView.append("热键:{0}+{1}注册{2}".format(modifier, key, "成功"))
        else:
            self.logView.append("热键:{0}+{1}注册{2}".format(modifier, key, "失败"))

    def onQuit(self):
        # 退出程序
        for kid in self.KeyIds:
            self.unregisterHotKey(kid)
        QApplication.instance().quit()

    def closeEvent(self, event):
        # 忽略关闭窗口,直接隐藏
        self.hide()
        return event.ignore()

    # 能监听热键,但是有个问题就是其它程序无法接受到事件
    # 比如Ctrl+S,在记事本里随便输入内容按下Ctrl+S发现无法保存
    def nativeEvent(self, eventType, message):
        if eventType == "windows_generic_MSG" or eventType == "windows_dispatcher_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            # 这段代码无法运行
            # if ctypes.windll.user32.GetMessageA(ctypes.byref(msg), None, 0,
            # 0) != 0:
            if msg.message == WM_HOTKEY:
                if msg.wParam == 1:  # Alt+S
                    self.show()
                self.logView.append("id:{0}, {1} at time:{2}".format(
                    msg.wParam, self.KeyIds.get(msg.wParam, None), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                return True, 0
        return super(Window, self).nativeEvent(eventType, message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.registerHotKey(1, "Alt", "S")
    w.registerHotKey(2, "Ctrl", "S")
    w.registerHotKey(3, "Shift", "S")
    w.registerHotKey(4, "Win", "S")
    w.registerHotKey(5, "Win", "Z")
    sys.exit(app.exec_())
