#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018年6月8日
author: Irony
site: https://pyqt.site , https://github.com/PyQt5
email: 892768447@qq.com
file: ProbeWindow
description: 简单探测窗口和放大截图
"""

import win32gui

try:
    from PyQt5.QtCore import Qt, QRect
    from PyQt5.QtGui import QPainter, QPen, QCursor, QColor
    from PyQt5.QtWidgets import QLabel, QWidget, QApplication
except ImportError:
    from PySide2.QtCore import Qt, QRect
    from PySide2.QtGui import QPainter, QPen, QCursor, QColor
    from PySide2.QtWidgets import QLabel, QWidget, QApplication


class FrameWidget(QWidget):
    # 一个全屏的透明窗口

    def __init__(self, *args, **kwargs):
        super(FrameWidget, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showFullScreen()  # 全屏
        self._rect = QRect()  # 被探测的窗口的矩形位置

    def setRect(self, x, y, w, h):
        # 更新矩形框
        self._rect.setX(x)
        self._rect.setY(y)
        self._rect.setWidth(w - x)
        self._rect.setHeight(h - y)
        self.update()

    def paintEvent(self, event):
        super(FrameWidget, self).paintEvent(event)
        if self._rect.isValid():  # 画边框
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 4))
            painter.drawRect(self._rect)


class Label(QLabel):

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.ismd = False  # 是不是否按下
        self.setAlignment(Qt.AlignCenter)
        self.setText('鼠标按住不放拖动到外面')
        self.resize(240, 240)
        self.frameWidget = FrameWidget()  # 边框

    def closeEvent(self, event):
        self.frameWidget.close()
        super(Label, self).closeEvent(event)

    def mousePressEvent(self, event):
        super(Label, self).mousePressEvent(event)
        self.ismd = True  # 按下
        # 设置鼠标样式为十字
        self.setCursor(Qt.CrossCursor)

    def mouseReleaseEvent(self, event):
        super(Label, self).mouseReleaseEvent(event)
        self.ismd = False
        self.frameWidget.setRect(0, 0, 0, 0)
        # 设置鼠标样式为普通
        self.setCursor(Qt.ArrowCursor)
        self.clear()
        self.setText('鼠标按住不放拖动到外面')

    def mouseMoveEvent(self, event):
        super(Label, self).mouseMoveEvent(event)
        # 得到鼠标在屏幕中的位置
        pos = self.mapToGlobal(event.pos())
        hwnd = win32gui.WindowFromPoint((pos.x(), pos.y()))
        self.frameWidget.setRect(*win32gui.GetWindowRect(hwnd))
        # 截图
        screen = QApplication.primaryScreen()
        if screen is not None:
            image = screen.grabWindow(0,
                                      pos.x() - 60, pos.y() - 60, 120, 120)
            if not image.isNull():
                self.setPixmap(image.scaled(240, 240))

    def paintEvent(self, event):
        super(Label, self).paintEvent(event)
        # 中正间画十字
        painter = QPainter(self)
        painter.setPen(Qt.red)
        x = int(self.width() / 2)
        y = int(self.height() / 2)
        painter.drawLine(x, 0, x, self.height())
        painter.drawLine(0, y, self.width(), y)
        if self.ismd:
            # 画坐标点
            pos = QCursor.pos()
            ret = win32gui.GetPixel(win32gui.GetWindowDC(
                win32gui.GetDesktopWindow()), pos.x(), pos.y())
            r, g, b = ret & 0xff, (ret >> 8) & 0xff, (ret >> 16) & 0xff
            print(r, g, b)
            painter.setPen(Qt.white)
            painter.drawText(self.rect(), Qt.AlignLeft |
                             Qt.AlignBottom, '({}, {})\nRGB: ({}, {}, {})\n{}'.format(
                pos.x(), pos.y(), r, g, b, QColor(r, g, b).name()))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    w = Label()
    w.show()
    sys.exit(app.exec_())
