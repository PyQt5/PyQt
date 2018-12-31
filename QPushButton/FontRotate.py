#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年2月1日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: PushButtonFont
@description: 
'''


import sys

from PyQt5.QtCore import QPropertyAnimation, Qt, QRectF
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QPushButton, QApplication, QStyleOptionButton,\
    QStylePainter, QStyle


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class PushButtonFont(QPushButton):

    LoadingText = "\uf110"

    def __init__(self, *args, **kwargs):
        super(PushButtonFont, self).__init__(*args, **kwargs)
        self.fontSize = self.font().pointSize() * 2
        self._rotateAnimationStarted = False
        self._rotateAnimation = QPropertyAnimation(self)
        self._rotateAnimation.setTargetObject(self)
        self._rotateAnimation.setStartValue(1)
        self._rotateAnimation.setEndValue(12)
        self._rotateAnimation.setDuration(1000)
        self._rotateAnimation.setLoopCount(-1)  # 无限循环
        self._rotateAnimation.valueChanged.connect(self.update)
        self.clicked.connect(self._onClick)

    def paintEvent(self, _):
        option = QStyleOptionButton()
        self.initStyleOption(option)
        painter = QStylePainter(self)
        if self._rotateAnimationStarted:
            option.text = ""
        painter.drawControl(QStyle.CE_PushButton, option)
        if not self._rotateAnimationStarted:
            return
        painter.save()
        font = self.font()
        font.setPointSize(self.fontSize)
        font.setFamily("FontAwesome")
        painter.setFont(font)
        # 变换坐标为正中间
        painter.translate(self.rect().center())
        # 旋转90度
        painter.rotate(self._rotateAnimation.currentValue() * 30)
        fm = self.fontMetrics()
        # 在变换坐标后的正中间画文字
        w = fm.width(self.LoadingText)
        h = fm.height()
        painter.drawText(
            QRectF(0 - w * 2, 0 - h, w * 2 * 2, h * 2), Qt.AlignCenter,
            self.LoadingText)
        painter.restore()

    def _onClick(self):
        if self._rotateAnimationStarted:
            self._rotateAnimationStarted = False
            self._rotateAnimation.stop()
            return
        self._rotateAnimationStarted = True
        self._rotateAnimation.start()

    def update(self, _=None):
        super(PushButtonFont, self).update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 加载字体到字体库中
    QFontDatabase.addApplicationFont(
        "Data/Fonts/FontAwesome/fontawesome-webfont.ttf")
    w = PushButtonFont("点击加载")
    w.resize(400, 400)
    w.show()
    sys.exit(app.exec_())
