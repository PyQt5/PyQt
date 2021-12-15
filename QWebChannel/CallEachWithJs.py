#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2021/12/15
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: CallEachWithJs.py
@description: 与JS之间的互相调用
"""

import os

from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (QApplication, QLineEdit, QPushButton, QVBoxLayout,
                             QWidget)

from Lib.WebChannelObject import WebChannelObject


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.m_obj = WebChannelObject(self)
        # 注册该窗口,可以访问该窗口的属性，槽函数，信号
        # https://doc.qt.io/qt-5/qwidget.html#properties
        # https://doc.qt.io/qt-5/qwidget.html#signals
        # https://doc.qt.io/qt-5/qwidget.html#public-slots
        self.m_obj.registerObject('qtwindow', self)
        self.m_obj.start()

        layout = QVBoxLayout(self)
        self.editTitle = QLineEdit(self, placeholderText='输入标题')
        layout.addWidget(self.editTitle)
        layout.addWidget(QPushButton('修改标题', self, clicked=self.onChangeTitle))

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                os.path.join(os.path.dirname(sys.argv[0] or __file__),
                             'Data/CallEachWithJs.html')))

    def onChangeTitle(self):
        self.setWindowTitle(self.editTitle.text())

    # ------- 把非槽函数通过pyqtSlot重新暴露 -------
    @pyqtSlot(int, int)
    def resize(self, width, height):
        super().resize(width, height)


if __name__ == '__main__':
    import cgitb
    import sys

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
