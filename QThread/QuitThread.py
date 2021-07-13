#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/11/27
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QuitThread
@description: 
"""

import sys
from time import time

try:
    from PyQt5.QtCore import QThread, QCoreApplication, QTimer
except ImportError:
    from PySide2.QtCore import QThread, QCoreApplication, QTimer


class Thread(QThread):

    def run(self):
        print('thread id', QThread.currentThread())
        i = 0
        while i < 101 and not self.isInterruptionRequested():
            print('value', i, time())
            i += 1
            QThread.msleep(500)
        print('thread quit')


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    t = Thread()
    t.finished.connect(app.quit)
    t.start()
    # 3秒后退出
    print('will quit 3s latter')
    QTimer.singleShot(3000, t.requestInterruption)
    sys.exit(app.exec_())
