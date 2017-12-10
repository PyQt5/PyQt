#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月10日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: DrawRectangle
@description: 
'''
import sys

from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath
from PyQt5.QtWidgets import QApplication, QDialog


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class DrawRectangle(QDialog):

    def __init__(self, *args, **kwargs):
        super(DrawRectangle, self).__init__(*args, **kwargs)
        self.pressed = False
        self.moved = False
        self.rectArea = QRect()  # 矩形框
        self.rectPen = QPen(QColor(22, 168, 250))
        self.rectPen.setWidth(1)
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showMaximized()
        # 通过绑定自定义右键菜单来监听右键点击,实现重新画区域或者退出,或者弹出菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onRightClicked)

    def onRightClicked(self, _):
        if not self.rectArea.isNull():
            self.rectArea.setWidth(0)
            self.rectArea.setHeight(0)  # clear
            return self.update()
        self.close()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.pressed = True
#             if not self.rectArea.isNull():
#                 self.moved = self.rectArea.contains(
#                     event.pos())  # 设置画好的窗口可整体移动
#                 return
            self.rectArea.setTopLeft(event.pos())  # 设置左上角位置

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.moved = False
        super(DrawRectangle, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.pos()
#         if self.moved and not self.rectArea.isNull():  # 表示移动整体画好的矩形框
#             # 重新设置矩形框的位置
#             self.rectArea.setX(pos.x())
#             self.rectArea.setY(pos.y())
#             return self.update()
        if not self.pressed:
            if not self.rectArea.isNull():
                if self.rectArea.contains(pos):
                    # 设置鼠标形状为十字箭头
                    return self.setCursor(Qt.SizeAllCursor)
            # 设置鼠标为普通形状
            return self.setCursor(Qt.ArrowCursor)
        self.rectArea.setBottomRight(pos)  # 设置右下角位置
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.rectArea.isNull():
            # 窗口背景全部半透明颜色
            return painter.fillRect(self.rect(), QColor(0, 0, 0, 50))

        # 画外围背景,去掉中间绘制的矩形框
        path = QPainterPath()
        path.setFillRule(Qt.OddEvenFill)
        path.addRect(QRectF(self.rect()))
        path.addRect(QRectF(self.rectArea))
        painter.fillPath(path, QColor(0, 0, 0, 50))
        # 画矩形
        painter.save()
        painter.setPen(self.rectPen)
        painter.drawRect(self.rectArea)  # 画矩形框
        # 背景用白色透明遮住,防止鼠标穿透到桌面
        painter.fillRect(self.rectArea, QColor(255, 255, 255, 1))
        painter.restore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DrawRectangle()
    w.show()
    sys.exit(app.exec_())
