#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021/1/1
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: DWaterProgress
@see https://github.com/linuxdeepin/dtkwidget/blob/master/src/widgets/dwaterprogress.cpp
@description:
"""
import math

try:
    from PyQt5.QtCore import pyqtSlot, QTimer, QSizeF, Qt, QRectF, QPointF, QRect, QPoint, QSize
    from PyQt5.QtGui import QImage, QColor, QPainter, QLinearGradient, QGradient, QPainterPath, QPixmap, \
        QBrush, QPen
    from PyQt5.QtSvg import QSvgRenderer
    from PyQt5.QtWidgets import QProgressBar, QGraphicsDropShadowEffect
except ImportError:
    from PySide2.QtCore import Slot as pyqtSlot, QTimer, QSizeF, Qt, QRectF, QPointF, QRect, QPoint, QSize
    from PySide2.QtGui import QImage, QColor, QPainter, QLinearGradient, QGradient, QPainterPath, QPixmap, \
        QBrush, QPen
    from PySide2.QtSvg import QSvgRenderer
    from PySide2.QtWidgets import QProgressBar, QGraphicsDropShadowEffect

WATER_FRONT = """<svg xmlns="http://www.w3.org/2000/svg" width="383" height="115" viewBox="0 0 383 115">
  <path fill="#01C4FF" fill-rule="evenodd" d="M383,115 L383,14.1688789 C380.269872,14.0716143 377.092672,13.5814974 373.063461,12.4722672 C368.696509,11.2699114 362.241136,10.1727531 357.649256,10.1227411 C347.007291,10.0071963 342.744795,10.6014761 332.930121,12.0276784 C326.157898,13.0120512 317.51313,12.4953762 311.375303,10.33762 C305.58601,8.30230681 299.587109,8.09191178 293.164466,8.16675723 C284.09108,8.27264456 276.303198,11.8021073 267.219716,11.3406179 C260.695053,11.0091595 256.565913,8.56512814 248.546835,8.86450991 C241.871757,9.11387975 235.569934,13.1896798 228.881972,13.3297132 C219.538394,13.525622 215.498041,10.7384053 208.282229,8.42337018 C201.688974,6.30769299 190.725982,6.45048568 185.454442,8.65549452 C170.142255,15.0597811 162.05946,9.31703167 150.536236,5.36712375 C147.826999,4.43862637 144.672431,3.20971247 141.663406,2.90998579 C135.153716,2.26155522 129.812539,3.9788615 123.613779,5.46231888 C115.747555,7.3451819 106.643181,6.73503633 99.4869089,3.84572629 C96.4124243,2.60474055 93.6255416,0.951587506 90.1882469,0.261077932 C79.652131,-1.85528907 69.7970674,9.59778831 58.8051757,9.35186757 C49.4744806,9.14319709 42.6942497,2.4740197 33.3934986,1.93078665 C20.5224457,1.17888312 19.3845731,15.343297 0,13.8463882 L0,115 L383,115 Z"/>
</svg>
"""
WATER_BACK = """<svg xmlns="http://www.w3.org/2000/svg" width="383" height="115" viewBox="0 0 383 115">
  <path fill="#007DFF" fill-rule="evenodd" d="M383,115 L383,14.1688789 C380.269872,14.0716143 377.092672,13.5814974 373.063461,12.4722672 C368.696509,11.2699114 362.241136,10.1727531 357.649256,10.1227411 C347.007291,10.0071963 342.744795,10.6014761 332.930121,12.0276784 C326.157898,13.0120512 317.51313,12.4953762 311.375303,10.33762 C305.58601,8.30230681 299.587109,8.09191178 293.164466,8.16675723 C284.09108,8.27264456 276.303198,11.8021073 267.219716,11.3406179 C260.695053,11.0091595 256.565913,8.56512814 248.546835,8.86450991 C241.871757,9.11387975 235.569934,13.1896798 228.881972,13.3297132 C219.538394,13.525622 215.498041,10.7384053 208.282229,8.42337018 C201.688974,6.30769299 190.725982,6.45048568 185.454442,8.65549452 C170.142255,15.0597811 162.05946,9.31703167 150.536236,5.36712375 C147.826999,4.43862637 144.672431,3.20971247 141.663406,2.90998579 C135.153716,2.26155522 129.812539,3.9788615 123.613779,5.46231888 C115.747555,7.3451819 106.643181,6.73503633 99.4869089,3.84572629 C96.4124243,2.60474055 93.6255416,0.951587506 90.1882469,0.261077932 C79.652131,-1.85528907 69.7970674,9.59778831 58.8051757,9.35186757 C49.4744806,9.14319709 42.6942497,2.4740197 33.3934986,1.93078665 C20.5224457,1.17888312 19.3845731,15.343297 0,13.8463882 L0,115 L383,115 Z"/>
</svg>
"""


class Pop:
    # https://github.com/linuxdeepin/dtkwidget/blob/master/src/widgets/dwaterprogress.cpp#L36

    def __init__(self, size, xs, ys, xo=0, yo=0):
        self.size = size
        self.xSpeed = xs
        self.ySpeed = ys
        self.xOffset = xo
        self.yOffset = yo


class DWaterProgress(QProgressBar):

    def __init__(self, *args, **kwargs):
        super(DWaterProgress, self).__init__(*args, **kwargs)
        self.waterFrontImage = QImage()
        self.waterBackImage = QImage()
        self.waterFrontSvg = QSvgRenderer(WATER_FRONT.encode())
        self.waterBackSvg = QSvgRenderer(WATER_BACK.encode())
        self.pops = []
        self.initPops()
        self.setTextVisible(True)
        self.interval = 33
        self.timer = QTimer(self)
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.onTimerOut)
        self.resizePixmap(self.size())
        self.frontXOffset = self.width()
        self.backXOffset = 0
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 6)
        effect.setColor(QColor(1, 153, 248, 255 * 5 / 20))
        effect.setBlurRadius(12)
        self.setGraphicsEffect(effect)

    def initPops(self):
        self.pops = [Pop(7, -1.8, 0.6), Pop(8, 1.2, 1.0), Pop(11, 0.8, 1.6)]

    @pyqtSlot()
    def start(self):
        self.timer.start()

    @pyqtSlot()
    def stop(self):
        self.timer.stop()

    def resizePixmap(self, sz):
        # https://github.com/linuxdeepin/dtkwidget/blob/master/src/widgets/dwaterprogress.cpp#L192
        # resize water
        waterWidth = 500 * sz.width() / 100
        waterHeight = 110 * sz.height() / 100
        waterSize = QSizeF(waterWidth, waterHeight).toSize()

        if self.waterFrontImage.size() != waterSize:
            image = QImage(waterWidth, waterHeight, QImage.Format_ARGB32)
            image.fill(Qt.transparent)
            waterPainter = QPainter(image)
            self.waterFrontSvg.render(waterPainter)
            self.waterFrontImage = image

        if self.waterBackImage.size() != waterSize:
            image = QImage(waterWidth, waterHeight, QImage.Format_ARGB32)
            image.fill(Qt.transparent)  # partly transparent red-ish background
            waterPainter = QPainter(image)
            self.waterBackSvg.render(waterPainter)
            self.waterBackImage = image

    def onTimerOut(self):
        # interval can not be zero, and limit to 1
        self.interval = max(1, self.interval)
        # move 60% per second
        frontXDeta = 40.0 / (1000.0 / self.interval)
        # move 90% per second
        backXDeta = 60.0 / (1000.0 / self.interval)

        canvasWidth = int(self.width() * self.devicePixelRatioF())
        self.frontXOffset -= frontXDeta * canvasWidth / 100
        self.backXOffset += backXDeta * canvasWidth / 100

        if self.frontXOffset > canvasWidth:
            self.frontXOffset = canvasWidth

        if self.frontXOffset < - (self.waterFrontImage.width() - canvasWidth):
            self.frontXOffset = canvasWidth

        if self.backXOffset > self.waterBackImage.width():
            self.backXOffset = 0

        # update pop
        # move 25% per second default
        speed = 25 / (1000.0 / self.interval)  # 100 / self.height()
        for pop in self.pops:
            # yOffset 0 ~ 100
            pop.yOffset += speed * pop.ySpeed
            if pop.yOffset < 0:
                pass
            if pop.yOffset > self.value():
                pop.yOffset = 0
            pop.xOffset = math.sin((pop.yOffset / 100) * 2 * 3.14) * 18 * pop.xSpeed + 50
        self.update()

    def paint(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)

        pixelRatio = self.devicePixelRatioF()
        rect = QRectF(0, 0, self.width() * pixelRatio, self.height() * pixelRatio)
        sz = QSizeF(self.width() * pixelRatio, self.height() * pixelRatio).toSize()

        self.resizePixmap(sz)

        yOffset = rect.toRect().topLeft().y() + (100 - self.value() - 10) * sz.height() / 100

        # draw water
        waterImage = QImage(sz, QImage.Format_ARGB32_Premultiplied)
        waterPainter = QPainter()
        waterPainter.begin(waterImage)
        waterPainter.setRenderHint(QPainter.Antialiasing)
        waterPainter.setCompositionMode(QPainter.CompositionMode_Source)

        pointStart = QPointF(sz.width() / 2, 0)
        pointEnd = QPointF(sz.width() / 2, sz.height())
        linear = QLinearGradient(pointStart, pointEnd)
        startColor = QColor('#1F08FF')
        startColor.setAlphaF(1)
        endColor = QColor('#50FFF7')
        endColor.setAlphaF(0.28)
        linear.setColorAt(0, startColor)
        linear.setColorAt(1, endColor)
        linear.setSpread(QGradient.PadSpread)
        waterPainter.setPen(Qt.NoPen)
        waterPainter.setBrush(linear)
        waterPainter.drawEllipse(waterImage.rect().center(), sz.width() / 2 + 1, sz.height() / 2 + 1)

        waterPainter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        waterPainter.drawImage(int(self.backXOffset), yOffset, self.waterBackImage)
        waterPainter.drawImage(int(self.backXOffset) - self.waterBackImage.width(), yOffset,
                               self.waterBackImage)
        waterPainter.drawImage(int(self.frontXOffset), yOffset, self.waterFrontImage)
        waterPainter.drawImage(int(self.frontXOffset) - self.waterFrontImage.width(), yOffset,
                               self.waterFrontImage)

        # draw pop
        if self.value() > 30:
            for pop in self.pops:
                popPath = QPainterPath()
                popPath.addEllipse(pop.xOffset * sz.width() / 100, (100 - pop.yOffset) * sz.height() / 100,
                                   pop.size * sz.width() / 100, pop.size * sz.height() / 100)
                waterPainter.fillPath(popPath, QColor(255, 255, 255, 255 * 0.3))

        if self.isTextVisible():
            font = waterPainter.font()
            rectValue = QRect()
            progressText = self.text().strip('%')

            if progressText == '100':
                font.setPixelSize(sz.height() * 35 / 100)
                waterPainter.setFont(font)

                rectValue.setWidth(sz.width() * 60 / 100)
                rectValue.setHeight(sz.height() * 35 / 100)
                rectValue.moveCenter(rect.center().toPoint())
                waterPainter.setPen(Qt.white)
                waterPainter.drawText(rectValue, Qt.AlignCenter, progressText)
            else:
                font.setPixelSize(sz.height() * 40 / 100)
                waterPainter.setFont(font)

                rectValue.setWidth(sz.width() * 45 / 100)
                rectValue.setHeight(sz.height() * 40 / 100)
                rectValue.moveCenter(rect.center().toPoint())
                rectValue.moveLeft(rect.left() + rect.width() * 0.45 * 0.5)

                waterPainter.setPen(Qt.white)
                waterPainter.drawText(rectValue, Qt.AlignCenter, progressText)
                font.setPixelSize(font.pixelSize() / 2)
                waterPainter.setFont(font)
                rectPerent = QRect(QPoint(rectValue.right(), rectValue.bottom() - rect.height() * 20 / 100),
                                   QPoint(rectValue.right() + rect.width() * 20 / 100, rectValue.bottom()))

                waterPainter.drawText(rectPerent, Qt.AlignCenter, '%')

        waterPainter.end()

        maskPixmap = QPixmap(sz)
        maskPixmap.fill(Qt.transparent)
        path = QPainterPath()
        path.addEllipse(QRectF(0, 0, sz.width(), sz.height()))
        maskPainter = QPainter()
        maskPainter.begin(maskPixmap)
        maskPainter.setRenderHint(QPainter.Antialiasing)
        maskPainter.setPen(QPen(Qt.white, 1))
        maskPainter.fillPath(path, QBrush(Qt.white))
        maskPainter.end()

        mode = QPainter.CompositionMode_SourceIn
        contentImage = QImage(sz, QImage.Format_ARGB32_Premultiplied)
        contentPainter = QPainter()
        contentPainter.begin(contentImage)
        contentPainter.setCompositionMode(QPainter.CompositionMode_Source)
        contentPainter.fillRect(contentImage.rect(), Qt.transparent)
        contentPainter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        contentPainter.drawImage(0, 0, maskPixmap.toImage())
        contentPainter.setCompositionMode(mode)
        contentPainter.drawImage(0, 0, waterImage)
        contentPainter.setCompositionMode(QPainter.CompositionMode_DestinationOver)
        contentPainter.end()

        contentImage.setDevicePixelRatio(pixelRatio)
        painter.drawImage(self.rect(), contentImage)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.paint(painter)

    def sizeHint(self):
        return QSize(100, 100)
