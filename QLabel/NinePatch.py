#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月25日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: NinePatch
@description: 
"""


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"

import sys

from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

from Lib.NinePatch import NinePatch


class Label(QWidget):

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        #.9 格式的图片
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
