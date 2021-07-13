#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年1月20日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: CircleImage
@description: 圆形图片
"""

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
    from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QApplication
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QPixmap, QPainter, QPainterPath
    from PySide2.QtWidgets import QLabel, QWidget, QHBoxLayout, QApplication


class Label(QLabel):

    def __init__(self, *args, antialiasing=True, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.Antialiasing = antialiasing
        self.setMaximumSize(200, 200)
        self.setMinimumSize(200, 200)
        self.radius = 100

        #####################核心实现#########################
        self.target = QPixmap(self.size())  # 大小和控件一样
        self.target.fill(Qt.transparent)  # 填充背景为透明

        p = QPixmap("Data/Images/head.jpg").scaled(  # 加载图片并缩放和控件一样大
            200, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        if self.Antialiasing:
            # 抗锯齿
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        #         painter.setPen(# 测试圆圈
        #             QPen(Qt.red, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        path = QPainterPath()
        path.addRoundedRect(
            0, 0, self.width(), self.height(), self.radius, self.radius)
        # **** 切割为圆形 ****#
        painter.setClipPath(path)
        #         painter.drawPath(path)  # 测试圆圈

        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)
        #####################核心实现#########################


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(Label(self))
        layout.addWidget(Label(self, antialiasing=False))
        self.setStyleSheet("background: black;")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
