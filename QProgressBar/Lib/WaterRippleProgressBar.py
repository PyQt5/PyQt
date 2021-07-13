#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年4月1日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: WaterRippleProgressBar
@description:
"""

import math

try:
    from PyQt5.QtCore import QTimer, Qt, QRectF, QSize
    from PyQt5.QtGui import QPainter, QPainterPath, QColor, QFont
    from PyQt5.QtWidgets import QProgressBar
except ImportError:
    from PySide2.QtCore import QTimer, Qt, QRectF, QSize
    from PySide2.QtGui import QPainter, QPainterPath, QColor, QFont
    from PySide2.QtWidgets import QProgressBar


class WaterRippleProgressBar(QProgressBar):
    # 浪高百分比
    waterHeight = 1
    # 密度
    waterDensity = 1
    # 样式1为矩形, 0为圆形
    styleType = 1
    # 文字颜色
    textColor = Qt.white
    # 背景颜色
    backgroundColor = Qt.gray
    # 波浪颜色1
    waterColor1 = QColor(33, 178, 148)
    # 波浪颜色2
    waterColor2 = QColor(33, 178, 148, 100)

    def __init__(self, *args, **kwargs):
        super(WaterRippleProgressBar, self).__init__(*args, **kwargs)
        self._offset = 0
        # 每隔100ms刷新波浪（模拟波浪动态）
        self._updateTimer = QTimer(self, timeout=self.update)
        self._updateTimer.start(100)

    def setRange(self, minValue, maxValue):
        if minValue == maxValue == 0:
            return  # 不允许设置busy状态
        super(WaterRippleProgressBar, self).setRange(minValue, maxValue)

    def setMinimum(self, value):
        if value == self.maximum() == 0:
            return  # 不允许设置busy状态
        super(WaterRippleProgressBar, self).setMinimum(value)

    def setMaximum(self, value):
        if value == self.minimum() == 0:
            return  # 不允许设置busy状态
        super(WaterRippleProgressBar, self).setMaximum(value)

    def setWaterHeight(self, height):
        """设置浪高"""
        self.waterHeight = height
        self.update()

    def setWaterDensity(self, density):
        """设置密度"""
        self.waterDensity = density
        self.update()

    def setStyleType(self, style):
        """设置类型"""
        self.styleType = style
        self.update()

    def sizeHint(self):
        return QSize(100, 100)

    def paintEvent(self, event):
        if self.minimum() == self.maximum() == 0:
            return
        # 正弦曲线公式 y = A * sin(ωx + φ) + k
        # 当前值所占百分比
        percent = 1 - (self.value() - self.minimum()) / \
                  (self.maximum() - self.minimum())
        # w表示周期，6为人为定义
        w = 6 * self.waterDensity * math.pi / self.width()
        # A振幅 高度百分比，1/26为人为定义
        A = self.height() * self.waterHeight * 1 / 26
        # k 高度百分比
        k = self.height() * percent

        # 波浪1
        waterPath1 = QPainterPath()
        waterPath1.moveTo(0, self.height())  # 起点在左下角
        # 波浪2
        waterPath2 = QPainterPath()
        waterPath2.moveTo(0, self.height())  # 起点在左下角

        # 偏移
        self._offset += 0.6
        if self._offset > self.width() / 2:
            self._offset = 0

        for i in range(self.width() + 1):
            # 从x轴开始计算y轴点
            y = A * math.sin(w * i + self._offset) + k
            waterPath1.lineTo(i, y)

            # 相对第一条需要进行错位
            y = A * math.sin(w * i + self._offset + self.width() / 2 * A) + k
            waterPath2.lineTo(i, y)

        # 封闭两条波浪，形成一个 U形 上面加波浪的封闭区间
        waterPath1.lineTo(self.width(), self.height())
        waterPath1.lineTo(0, self.height())
        waterPath2.lineTo(self.width(), self.height())
        waterPath2.lineTo(0, self.height())

        # 整体形状（矩形或者圆形）
        bgPath = QPainterPath()
        if self.styleType:
            bgPath.addRect(QRectF(self.rect()))
        else:
            radius = min(self.width(), self.height())
            bgPath.addRoundedRect(QRectF(self.rect()), radius, radius)

        # 开始画路径
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        # 设置没有画笔
        painter.setPen(Qt.NoPen)

        if not self.styleType:
            # 圆形
            painter.setClipPath(bgPath)

        # 先整体绘制背景，然后再在背景上方绘制两条波浪
        painter.save()
        painter.setBrush(self.backgroundColor)
        painter.drawPath(bgPath)
        painter.restore()

        # 波浪1
        painter.save()
        painter.setBrush(self.waterColor1)
        painter.drawPath(waterPath1)
        painter.restore()

        # 波浪2
        painter.save()
        painter.setBrush(self.waterColor2)
        painter.drawPath(waterPath2)
        painter.restore()

        # 绘制文字
        if not self.isTextVisible():
            return
        painter.setPen(self.textColor)
        font = self.font() or QFont()
        font.setPixelSize(int(min(self.width(), self.height()) / 2))
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, '%d%%' %
                         (self.value() / self.maximum() * 100))
