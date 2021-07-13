#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年3月8日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: Threading.QtThreading
@description: 
"""
from threading import Thread
from time import sleep

try:
    from PyQt5.QtCore import QObject, pyqtSignal, QTimer, Qt
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QApplication
except ImportError:
    from PySide2.QtCore import QObject, Signal as pyqtSignal, QTimer, Qt
    from PySide2.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QApplication


class _Signals(QObject):
    updateProgress = pyqtSignal(int)


Signals = _Signals()


class UpdateThread(Thread):

    def run(self):
        self.i = 0
        for i in range(101):
            self.i += 1
            Signals.updateProgress.emit(i)
            sleep(1)
        self.i = 0
        Signals.updateProgress.emit(i)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        layout = QVBoxLayout(self)
        self.progressBar = QProgressBar(self)
        layout.addWidget(self.progressBar)
        Signals.updateProgress.connect(
            self.progressBar.setValue, type=Qt.QueuedConnection)

        QTimer.singleShot(2000, self.doStart)

    def doStart(self):
        self.updateThread = UpdateThread(daemon=True)
        self.updateThread.start()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
