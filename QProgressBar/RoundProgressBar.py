#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年9月4日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: 界面美化.圆形进度条.CircleProgressBar
@description: 
"""

try:
    from PyQt5.QtCore import QSize, pyqtProperty, QTimer, Qt
    from PyQt5.QtGui import QColor, QPainter
    from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
except ImportError:
    from PySide2.QtCore import QSize, Property as pyqtProperty, QTimer, Qt
    from PySide2.QtGui import QColor, QPainter
    from PySide2.QtWidgets import QApplication, QWidget, QHBoxLayout


class CircleProgressBar(QWidget):
    Color = QColor(24, 189, 155)  # 圆圈颜色
    Clockwise = True  # 顺时针还是逆时针
    Delta = 36

    def __init__(self, *args, color=None, clockwise=True, **kwargs):
        super(CircleProgressBar, self).__init__(*args, **kwargs)
        self.angle = 0
        self.Clockwise = clockwise
        if color:
            self.Color = color
        self._timer = QTimer(self, timeout=self.update)
        self._timer.start(100)

    def paintEvent(self, event):
        super(CircleProgressBar, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        side = min(self.width(), self.height())
        painter.scale(side / 100.0, side / 100.0)
        painter.rotate(self.angle)
        painter.save()
        painter.setPen(Qt.NoPen)
        color = self.Color.toRgb()
        for i in range(11):
            color.setAlphaF(1.0 * i / 10)
            painter.setBrush(color)
            painter.drawEllipse(30, -10, 20, 20)
            painter.rotate(36)
        painter.restore()
        self.angle += self.Delta if self.Clockwise else -self.Delta
        self.angle %= 360

    @pyqtProperty(QColor)
    def color(self) -> QColor:
        return self.Color

    @color.setter
    def color(self, color: QColor):
        if self.Color != color:
            self.Color = color
            self.update()

    @pyqtProperty(bool)
    def clockwise(self) -> bool:
        return self.Clockwise

    @clockwise.setter
    def clockwise(self, clockwise: bool):
        if self.Clockwise != clockwise:
            self.Clockwise = clockwise
            self.update()

    @pyqtProperty(int)
    def delta(self) -> int:
        return self.Delta

    @delta.setter
    def delta(self, delta: int):
        if self.delta != delta:
            self.delta = delta
            self.update()

    def sizeHint(self) -> QSize:
        return QSize(100, 100)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(CircleProgressBar(self))
        layout.addWidget(CircleProgressBar(
            self, color=QColor(255, 0, 0), clockwise=False))
        layout.addWidget(CircleProgressBar(self, styleSheet="""
            qproperty-color: rgb(0, 255, 0);
        """))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
