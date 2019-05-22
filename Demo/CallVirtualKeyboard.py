#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年5月22日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Demo.CallVirtualKeyboard
@description: 调用系统虚拟键盘
"""
import glob

from PyQt5.QtCore import QProcess, QSysInfo
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QPushButton


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.resultEdit = QTextEdit(self)
        self.resultEdit.setReadOnly(True)
        layout.addWidget(self.resultEdit)
        layout.addWidget(QPushButton(
            '打开虚拟键盘', self, clicked=self._onOpenKeyboard))

    def _onOpenKeyboard(self):
        kernelType = QSysInfo.kernelType()
        if kernelType == 'winnt':
            try:
                path = glob.glob(
                    r'C:\Windows\WinSxS\amd64_microsoft-windows-osk_*\osk.exe')[0]
                ret = QProcess.startDetached(path)
                self.resultEdit.append('start 64 osk: %s' % ret)
            except Exception as e:
                self.resultEdit.append('start osk error: %s' % e)
            try:
                # 32位程序调用64位操作系统下的程序会被重定向到SysWOW64目录
                # 可通过`Wow64DisableWow64FsRedirection`和`Wow64RevertWow64FsRedirection`控制
                ret = QProcess.startDetached(r'C:\Windows\system32\osk.exe')
                self.resultEdit.append('start 32 osk: %s' % ret)
            except Exception as e:
                self.resultEdit.append('start osk error: %s' % e)
        elif kernelType == 'darwin':
            pass
#         elif kernelType=='linux':
        else:
            ret = QProcess.startDetached('florence')
            self.resultEdit.append('start florence: %s' % ret)
            ret = QProcess.startDetached('onboard')
            self.resultEdit.append('start onboard: %s' % ret)
            ret = QProcess.startDetached('kvkbd')
            self.resultEdit.append('start kvkbd: %s' % ret)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
