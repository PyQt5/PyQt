#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020年3月13日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: Demo.GifCursor
@description: 
"""

try:
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
except ImportError:
    from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication

from Lib.QCursorGif import QCursorGif


class Window(QWidget, QCursorGif):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # 设置忙碌光标图片数组
        self.initCursor(['Data/Images/Cursors/%d.png' %
                         i for i in range(8)], self)
        self.setCursorTimeout(100)

        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton(
            'start busy', self, clicked=self.startBusy))
        layout.addWidget(QPushButton(
            'stop busy', self, clicked=self.stopBusy))


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
