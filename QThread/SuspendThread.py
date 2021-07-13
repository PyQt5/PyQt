#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月13日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file:
@description:
"""

import ctypes

import win32con
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QPushButton
from win32process import SuspendThread, ResumeThread


class Worker(QThread):
    valueChanged = pyqtSignal(int)  # 值变化信号
    handle = -1

    def run(self):
        try:
            self.handle = ctypes.windll.kernel32.OpenThread(  # @UndefinedVariable
                win32con.PROCESS_ALL_ACCESS, False, int(QThread.currentThreadId()))
        except Exception as e:
            print('get thread handle failed', e)
        print('thread id', int(QThread.currentThreadId()))
        for i in range(1, 101):
            print('value', i)
            self.valueChanged.emit(i)
            QThread.sleep(1)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)
        layout.addWidget(self.progressBar)
        self.startButton = QPushButton('开启线程', self, clicked=self.onStart)
        layout.addWidget(self.startButton)
        self.suspendButton = QPushButton(
            '挂起线程', self, clicked=self.onSuspendThread, enabled=False)
        layout.addWidget(self.suspendButton)
        self.resumeButton = QPushButton(
            '恢复线程', self, clicked=self.onResumeThread, enabled=False)
        layout.addWidget(self.resumeButton)
        self.stopButton = QPushButton(
            '终止线程', self, clicked=self.onStopThread, enabled=False)
        layout.addWidget(self.stopButton)

        # 当前线程id
        print('main id', int(QThread.currentThreadId()))

        # 子线程
        self._thread = Worker(self)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.valueChanged.connect(self.progressBar.setValue)

    def onStart(self):
        print('main id', int(QThread.currentThreadId()))
        self._thread.start()  # 启动线程
        self.startButton.setEnabled(False)
        self.suspendButton.setEnabled(True)
        self.stopButton.setEnabled(True)

    def onSuspendThread(self):
        if self._thread.handle == -1:
            return print('handle is wrong')
        ret = SuspendThread(self._thread.handle)
        print('挂起线程', self._thread.handle, ret)
        self.suspendButton.setEnabled(False)
        self.resumeButton.setEnabled(True)

    def onResumeThread(self):
        if self._thread.handle == -1:
            return print('handle is wrong')
        ret = ResumeThread(self._thread.handle)
        print('恢复线程', self._thread.handle, ret)
        self.suspendButton.setEnabled(True)
        self.resumeButton.setEnabled(False)

    def onStopThread(self):
        self.startButton.setEnabled(False)
        self.suspendButton.setEnabled(False)
        self.resumeButton.setEnabled(False)
        ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
            self._thread.handle, 0)
        print('终止线程', self._thread.handle, ret)
        self.stopButton.setEnabled(False)

    def closeEvent(self, event):
        if self._thread.isRunning():
            self._thread.quit()
            # 强制
            # self._thread.terminate()
        del self._thread
        super(Window, self).closeEvent(event)


if __name__ == '__main__':
    import sys
    import os

    print('pid', os.getpid())
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
