#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年5月15日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: FlipWidget
@description: 动画翻转窗口
"""

try:
    from PyQt5.QtCore import pyqtSignal, pyqtProperty, Qt, QPropertyAnimation, QEasingCurve, QPointF
    from PyQt5.QtGui import QPainter, QTransform
    from PyQt5.QtWidgets import QWidget
except ImportError:
    from PySide2.QtCore import Signal as pyqtSignal, Property as pyqtProperty, Qt, QPropertyAnimation, \
        QEasingCurve, QPointF
    from PySide2.QtGui import QPainter, QTransform
    from PySide2.QtWidgets import QWidget


class FlipWidget(QWidget):
    Left = 0  # 从右往左
    Right = 1  # 从左往右
    Scale = 3  # 图片缩放比例
    finished = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(FlipWidget, self).__init__(*args, **kwargs)
        # 无边框无任务栏
        self.setWindowFlags(self.windowFlags() |
                            Qt.FramelessWindowHint | Qt.SubWindow)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 翻转角度
        self._angle = 0
        # 属性动画针对自定义属性`angle`
        self._animation = QPropertyAnimation(self, b'angle', self)
        self._animation.setDuration(550)
        self._animation.setEasingCurve(QEasingCurve.OutInQuad)
        self._animation.finished.connect(self.finished.emit)

    @pyqtProperty(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self.update()

    def updateImages(self, direction, image1, image2):
        """设置两张切换图
        :param direction:        方向
        :param image1:           图片1
        :param image2:           图片2
        """
        self.image1 = image1
        self.image2 = image2
        self.show()
        self._angle = 0
        # 根据方向设置动画的初始和结束值
        if direction == self.Right:
            self._animation.setStartValue(1)
            self._animation.setEndValue(-180)
        elif direction == self.Left:
            self._animation.setStartValue(1)
            self._animation.setEndValue(180)
        self._animation.start()

    def paintEvent(self, event):
        super(FlipWidget, self).paintEvent(event)

        if hasattr(self, 'image1') and hasattr(self, 'image2') and self.isVisible():

            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            # 变换
            transform = QTransform()
            # 把圆心设置为矩形中心
            transform.translate(self.width() / 2, self.height() / 2)

            if self._angle >= -90 and self._angle <= 90:
                # 当翻转角度在90范围内显示第一张图，且从大图缩放到小图的过程
                painter.save()
                # 设置翻转角度
                transform.rotate(self._angle, Qt.YAxis)
                painter.setTransform(transform)
                # 缩放图片高度
                width = self.image1.width() / 2
                height = int(self.image1.height() *
                             (1 - abs(self._angle / self.Scale) / 100))
                image = self.image1.scaled(
                    self.image1.width(), height,
                    Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                painter.drawPixmap(
                    QPointF(-width, -height / 2), image)
                painter.restore()
            else:
                # 当翻转角度在90范围内显示第二张图，且从小图缩放到原图的过程
                painter.save()
                if self._angle > 0:
                    angle = 180 + self._angle
                else:
                    angle = self._angle - 180
                # 设置翻转角度， 注意这里角度有差异
                transform.rotate(angle, Qt.YAxis)
                painter.setTransform(transform)
                # 缩放图片高度
                width = self.image2.width() / 2
                height = int(self.image2.height() *
                             (1 - ((360 - abs(angle)) / self.Scale / 100)))
                image = self.image2.scaled(
                    self.image2.width(), height,
                    Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                painter.drawPixmap(
                    QPointF(-width, -height / 2), image)
                painter.restore()
