#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年9月25日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: AnimationShadowEffect
@description: 边框动画阴影动画
"""

try:
    from PyQt5.QtCore import QPropertyAnimation, pyqtProperty
    from PyQt5.QtWidgets import QGraphicsDropShadowEffect
except ImportError:
    from PySide2.QtCore import QPropertyAnimation, Property as pyqtProperty
    from PySide2.QtWidgets import QGraphicsDropShadowEffect


class AnimationShadowEffect(QGraphicsDropShadowEffect):

    def __init__(self, color, *args, **kwargs):
        super(AnimationShadowEffect, self).__init__(*args, **kwargs)
        self.setColor(color)
        self.setOffset(0, 0)
        self.setBlurRadius(0)
        self._radius = 0
        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setDuration(2000)  # 一次循环时间
        self.animation.setLoopCount(-1)  # 永久循环
        self.animation.setPropertyName(b'radius')
        # 插入值
        self.animation.setKeyValueAt(0, 1)
        self.animation.setKeyValueAt(0.5, 30)
        self.animation.setKeyValueAt(1, 1)

    def start(self):
        self.animation.start()

    def stop(self, r=0):
        # 停止动画并修改半径值
        self.animation.stop()
        self.radius = r

    @pyqtProperty(int)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = r
        self.setBlurRadius(r)
