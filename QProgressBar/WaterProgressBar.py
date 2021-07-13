#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年4月1日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: WaterProgressBar
@description:
"""

from random import randint

try:
    from PyQt5.QtCore import QTimer
    from PyQt5.QtGui import QPixmap, QIcon
    from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QRadioButton, QPushButton, QColorDialog, \
        QSpinBox
except ImportError:
    from PySide2.QtCore import QTimer
    from PySide2.QtGui import QPixmap, QIcon
    from PySide2.QtWidgets import QApplication, QWidget, QFormLayout, QRadioButton, QPushButton, QColorDialog, \
        QSpinBox

from Lib.WaterRippleProgressBar import WaterRippleProgressBar  # @UnresolvedImport


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)

        self.bar = WaterRippleProgressBar(self)
        self.bar.setMinimumSize(400, 400)
        self.bar.setMaximumSize(400, 400)

        layout = QFormLayout(self)

        layout.addWidget(QRadioButton(
            '矩形', self, checked=True, clicked=lambda: self.bar.setStyleType(1)))
        layout.addWidget(
            QRadioButton('圆形', clicked=lambda: self.bar.setStyleType(0)))
        layout.addWidget(
            QPushButton('设置背景颜色', self, clicked=self.chooseBackgroundColor))
        layout.addWidget(
            QPushButton('设置文字颜色', self, clicked=self.chooseTextColor))
        layout.addWidget(
            QPushButton('设置波浪1颜色', self, clicked=self.chooseWaterColor1))
        layout.addWidget(
            QPushButton('设置波浪2颜色', self, clicked=self.chooseWaterColor2))
        layout.addWidget(
            QPushButton('设置随机0-100固定值', self, clicked=self.setRandomValue))

        spb1 = QSpinBox(self, value=1)
        spb1.valueChanged.connect(self.bar.setWaterHeight)
        layout.addRow('振幅(浪高)', spb1)

        spb2 = QSpinBox(self, value=1)
        spb2.valueChanged.connect(self.bar.setWaterDensity)
        layout.addRow('周期(密度)', spb2)

        layout.addWidget(self.bar)

        # 动态设置进度条的值
        self._valueTimer = QTimer(self, timeout=self.updateValue)
        self._valueTimer.start(100)

    def chooseBackgroundColor(self):
        """设置背景颜色"""
        col = QColorDialog.getColor(self.bar.backgroundColor, self)
        if not col.isValid():
            return
        self.bar.backgroundColor = col
        pix = QPixmap(16, 16)
        pix.fill(col)
        self.sender().setIcon(QIcon(pix))

    def chooseTextColor(self):
        """设置文字颜色"""
        col = QColorDialog.getColor(self.bar.textColor, self)
        if not col.isValid():
            return
        self.bar.textColor = col
        pix = QPixmap(16, 16)
        pix.fill(col)
        self.sender().setIcon(QIcon(pix))

    def chooseWaterColor1(self):
        """设置波浪1颜色"""
        col = QColorDialog.getColor(self.bar.waterColor1, self)
        if not col.isValid():
            return
        self.bar.waterColor1 = col
        pix = QPixmap(16, 16)
        pix.fill(col)
        self.sender().setIcon(QIcon(pix))

    def chooseWaterColor2(self):
        """设置波浪2颜色"""
        col = QColorDialog.getColor(self.bar.waterColor2, self)
        if not col.isValid():
            return
        self.bar.waterColor2 = col
        pix = QPixmap(16, 16)
        pix.fill(col)
        self.sender().setIcon(QIcon(pix))

    def setRandomValue(self):
        """设置随机0-100值，并停止自增"""
        self._valueTimer.stop()
        self.bar.setValue(randint(0, 100))

    def updateValue(self):
        value = self.bar.value() + 1
        if value > self.bar.maximum():
            value = 0
        self.bar.setValue(value)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
