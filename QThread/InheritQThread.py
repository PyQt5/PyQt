#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月9日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: InheritQThread
@description: 继承QThread
"""

try:
    from PyQt5.QtCore import QThread, pyqtSignal
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton
except ImportError:
    from PySide2.QtCore import QThread, Signal as pyqtSignal
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton


class Worker(QThread):
    valueChanged = pyqtSignal(int)  # 值变化信号

    def run(self):
        print('thread id', QThread.currentThread())
        for i in range(1, 101):
            if self.isInterruptionRequested():
                break
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
        layout.addWidget(QPushButton('开启线程', self, clicked=self.onStart))

        # 当前线程id
        print('main id', QThread.currentThread())

        # 子线程
        self._thread = Worker(self)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.valueChanged.connect(self.progressBar.setValue)

    def onStart(self):
        if not self._thread.isRunning():
            print('main id', QThread.currentThread())
            self._thread.start()  # 启动线程

    def closeEvent(self, event):
        if self._thread.isRunning():
            self._thread.requestInterruption()
            self._thread.quit()
            self._thread.wait()
            # 强制
            # self._thread.terminate()
        self._thread.deleteLater()
        super(Window, self).closeEvent(event)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
