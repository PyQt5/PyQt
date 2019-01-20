#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年3月30日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: TestQSingleApplication
@description: 
'''
from PyQt5.QtWidgets import QTextEdit

from Lib.Application import QSingleApplication  # @UnresolvedImport


__version__ = "0.0.1"

class Widget(QTextEdit):
    
    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)

if __name__ == "__main__":
    import sys
    app = QSingleApplication(sys.argv)
    if app.isRunning():
        app.sendMessage("app is running")
        sys.exit(0)
    t = Widget()
    app.setActivationWindow(t)
    app.messageReceived.connect(t.append)
    t.show()
    sys.exit(app.exec_())
