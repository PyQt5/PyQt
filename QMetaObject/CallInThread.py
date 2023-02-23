#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2023/02/23
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: CallInThread.py
@description:
"""
import time
from datetime import datetime
from threading import Thread

from PyQt5.QtCore import (Q_ARG, Q_RETURN_ARG, QMetaObject, Qt, QThread,
                          pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QTextBrowser, QWidget


class ThreadQt(QThread):

    def __init__(self, textBrowser, *args, **kwargs):
        super(ThreadQt, self).__init__(*args, **kwargs)
        self._textBrowser = textBrowser

    def stop(self):
        self.requestInterruption()

    def run(self):
        while not self.isInterruptionRequested():
            text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 通过`invokeMethod`直接调用对应的槽函数
            # 1. 获取函数`isReadOnly1`返回值, self.parent() 是Window窗口对象
            # NOTE：注意这里获取返回值要用 `Qt.DirectConnection` 方式
            retValue = QMetaObject.invokeMethod(self.parent(), 'isReadOnly1',
                                                Qt.DirectConnection,
                                                Q_RETURN_ARG(bool))
            # 2. 通过`invokeMethod`队列调用对应控件槽函数`append`
            argValue = Q_ARG(str, text + ' readOnly: ' + str(retValue))
            QMetaObject.invokeMethod(self._textBrowser, 'append',
                                     Qt.QueuedConnection, argValue)
            self.sleep(1)


class ThreadPy(Thread):

    def __init__(self, textBrowser, parent, *args, **kwargs):
        super(ThreadPy, self).__init__(*args, **kwargs)
        self._running = True
        self._textBrowser = textBrowser
        self._parent = parent

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 通过`invokeMethod`队列调用对应控件信号，`self._parent`是Window窗口对象
            QMetaObject.invokeMethod(self._parent, 'appendText',
                                     Qt.QueuedConnection,
                                     Q_ARG(str, text + ' from Signal'))
            # 通过`invokeMethod`队列调用对应控件槽函数`append`
            QMetaObject.invokeMethod(self._textBrowser, 'append',
                                     Qt.QueuedConnection,
                                     Q_ARG(str, text + ' to Slot'))
            time.sleep(1)


class Window(QWidget):

    # 更新信号
    appendText = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        self.textBrowser1 = QTextBrowser(self)
        self.textBrowser2 = QTextBrowser(self)
        layout.addWidget(self.textBrowser1)
        layout.addWidget(self.textBrowser2)

        self.appendText.connect(self.textBrowser2.append)

        # Qt线程
        self.thread1 = ThreadQt(self.textBrowser1, self)
        self.thread1.start()

        # PY线程
        self.thread2 = ThreadPy(self.textBrowser2, self)
        self.thread2.start()

    @pyqtSlot(result=bool)
    def isReadOnly1(self):
        # 线程中直接调用该槽函数获取UI中的内容
        return self.textBrowser1.isReadOnly()

    def closeEvent(self, event):
        self.thread1.stop()
        self.thread2.stop()
        self.thread1.wait()
        self.thread2.join()
        super(Window, self).closeEvent(event)


if __name__ == '__main__':
    import cgitb
    import sys

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
