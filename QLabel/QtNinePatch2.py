#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月25日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: QtNinePatch2
@description: 
"""


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"

import sys

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication, QLabel

from Lib import QtNinePatch2


class Label(QLabel):

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        #.9 格式的图片
        self.image = QImage('Data/skin_aio_friend_bubble_pressed.9.png')

    def showEvent(self, event):
        super(Label, self).showEvent(event)
        pixmap = QtNinePatch2.createPixmapFromNinePatchImage(
            self.image, self.width(), self.height())
        self.setPixmap(pixmap)

    def resizeEvent(self, event):
        super(Label, self).resizeEvent(event)
        pixmap = QtNinePatch2.createPixmapFromNinePatchImage(
            self.image, self.width(), self.height())
        self.setPixmap(pixmap)


app = QApplication(sys.argv)
w = Label()
w.resize(400, 200)
w.show()

sys.exit(app.exec_())
