#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020年3月13日
@author: Irony
@site: https://pyqt.site https://github.com/892768447
@email: 892768447@qq.com
@file: Demo.GifCursor
@description: 
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from Lib.QCursorGif import QCursorGif


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2020'
__Version__ = 1.0


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
    cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
