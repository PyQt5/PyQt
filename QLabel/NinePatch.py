#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月25日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: NinePatch
@description: 
"""

import sys

try:
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QApplication, QWidget
except ImportError:
    from PySide2.QtGui import QPainter
    from PySide2.QtWidgets import QApplication, QWidget

from Lib.NinePatch import NinePatch


class Label(QWidget):

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        # .9 格式的图片
        self.image = NinePatch('Data/skin_aio_friend_bubble_pressed.9.png')

    def paintEvent(self, event):
        super(Label, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        try:
            self.image.SetImageSize(self.width(), self.height())
            self.image.Draw(painter, 0, 0)
        except Exception as e:
            print(e)


app = QApplication(sys.argv)
w = Label()
w.resize(400, 200)
w.show()

sys.exit(app.exec_())
