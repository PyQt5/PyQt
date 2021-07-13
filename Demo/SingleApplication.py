#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年3月30日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: TestQSingleApplication
@description: 
"""

from PyQt5.QtWidgets import QTextEdit

from Lib.Application import QSingleApplication  # @UnresolvedImport


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
