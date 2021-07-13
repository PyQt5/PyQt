#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年3月30日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: TestQSharedMemory
@description: 
"""

from PyQt5.QtWidgets import QWidget

from Lib.Application import SharedApplication  # @UnresolvedImport


class Widget(QWidget):

    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)


if __name__ == "__main__":
    import sys, os

    print(os.getpid())
    app = SharedApplication(sys.argv)
    if app.isRunning():
        print("app have already running")
        sys.exit(0)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
