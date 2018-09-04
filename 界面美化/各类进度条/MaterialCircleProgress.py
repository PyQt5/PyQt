#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年9月4日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: 界面美化.各类进度条.MaterialCircleProgress
@description: 
"""
from PyQt5.QtCore import pyqtProperty, QSize, QParallelAnimationGroup,\
    QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class MaterialCircleProgress(QWidget):

    BorderWidth = 6.25  # 边框宽度
    BorderColor = QColor(24, 189, 155)  # 边框颜色
    DashLength = 0
    DashOffset = 0
    Angle = 0

    def __init__(self, *args, **kwargs):
        super(MaterialCircleProgress, self).__init__(*args, **kwargs)
        self.initAnimation()

    def initAnimation(self):
        # 动画组
        self._animationGroup = QParallelAnimationGroup(self, loopCount=-1)

        animation = QPropertyAnimation(self, b'dashLength', self)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.setStartValue(0.1)
        animation.setKeyValueAt(0.15, 0.2)
        animation.setKeyValueAt(0.6, 20)
        animation.setKeyValueAt(0.7, 20)
        animation.setEndValue(20)
        animation.setDuration(2050)
        self._animationGroup.addAnimation(animation)

        animation = QPropertyAnimation(self, b'dashOffset', self)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        animation.setStartValue(0)
        animation.setKeyValueAt(0.15, 0)
        animation.setKeyValueAt(0.6, -7)
        animation.setKeyValueAt(0.7, -7)
        animation.setEndValue(-25)
        animation.setDuration(2050)
        self._animationGroup.addAnimation(animation)

        animation = QPropertyAnimation(self, b'angle', self)
        animation.setStartValue(0)
        animation.setEndValue(719)
        animation.setDuration(2050)
        self._animationGroup.addAnimation(animation)
        
        self._animationGroup.start()

    @pyqtProperty(float)
    def dashLength(self) -> float:
        return self.DashLength

    @dashLength.setter
    def dashLength(self, dashLength: float):
        if self.DashLength != dashLength:
            self.DashLength = dashLength
            self.update()

    @pyqtProperty(float)
    def dashOffset(self) -> float:
        return self.DashOffset

    @dashOffset.setter
    def dashOffset(self, dashOffset: float):
        if self.DashOffset != dashOffset:
            self.DashOffset = dashOffset
            self.update()

    @pyqtProperty(int)
    def angle(self) -> int:
        return self.Angle

    @angle.setter
    def angle(self, angle: int):
        if self.Angle != angle:
            self.Angle = angle
            self.update()

    @pyqtProperty(float)
    def borderWidth(self) -> float:
        return self.BorderWidth

    @borderWidth.setter
    def borderWidth(self, borderWidth: float):
        if self.BorderWidth != borderWidth:
            self.BorderWidth = borderWidth
            self.update()

    @pyqtProperty(QColor)
    def borderColor(self) -> QColor:
        return self.BorderColor

    @borderColor.setter
    def borderColor(self, borderColor: QColor):
        if self.BorderColor != borderColor:
            self.BorderColor = borderColor
            self.update()

    def sizeHint(self) -> QSize:
        return QSize(100, 100)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
