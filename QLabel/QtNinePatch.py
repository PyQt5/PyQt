#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月25日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: testQtNinePatch
@description: 
"""

import sys
from ctypes import CDLL

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication, QLabel

CDLL('Lib/QtNinePatch/sip/QtNinePatch.dll')

from Lib.QtNinePatch.sip.QtNinePatch import QtNinePatch


class Label(QLabel):

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        # .9 格式的图片
        self.image = QImage('Data/skin_aio_friend_bubble_pressed.9.png')

    def showEvent(self, event):
        super(Label, self).showEvent(event)
        pixmap = QtNinePatch.createPixmapFromNinePatchImage(
            self.image, self.width(), self.height())
        self.setPixmap(pixmap)

    def resizeEvent(self, event):
        super(Label, self).resizeEvent(event)
        pixmap = QtNinePatch.createPixmapFromNinePatchImage(
            self.image, self.width(), self.height())
        self.setPixmap(pixmap)


app = QApplication(sys.argv)
w = Label()
w.resize(400, 200)
w.show()

sys.exit(app.exec_())
