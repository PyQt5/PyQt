#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月11日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: 
@description: 
"""
from PyQt5.QtCore import QThread, QWaitCondition, QMutex, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QProgressBar


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class Thread(QThread):

    valueChange = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self._isPause = False
        self._value = 0
        self.cond = QWaitCondition()
        self.mutex = QMutex()

    def pause(self):
        self._isPause = True

    def resume(self):
        self._isPause = False
        self.cond.wakeAll()

    def run(self):
        while 1:
            self.mutex.lock()
            if self._isPause:
                self.cond.wait(self.mutex)
            if self._value > 100:
                self._value = 0
            self._value += 1
            self.valueChange.emit(self._value)
            self.msleep(100)
            self.mutex.unlock()


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.progressBar = QProgressBar(self)
        layout.addWidget(self.progressBar)
        layout.addWidget(QPushButton('休眠', self, clicked=self.doWait))
        layout.addWidget(QPushButton('唤醒', self, clicked=self.doWake))

        self.t = Thread(self)
        self.t.valueChange.connect(self.progressBar.setValue)
        self.t.start()

    def doWait(self):
        self.t.pause()

    def doWake(self):
        self.t.resume()


if __name__ == '__main__':
    import sys
    import cgitb
    cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
