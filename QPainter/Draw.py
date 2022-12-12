#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2022年12月12日
@site: https://pyqt.site , https://github.com/PyQt5
@description: QPainter画图
"""
import sys
try:
    from PyQt5.QtWidgets import QApplication, QWidget, qApp
    from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap
    from PyQt5.QtCore import Qt, pyqtSignal
    from PyQt5.Qt import QPoint, QPolygon
except ImportError:
    from PySide2.QtWidgets import QApplication, QWidget, qApp
    from PySide2.QtGui import QPainter, QFont, QColor, QPixmap
    from PySide2.QtCore import Qt, pyqtSignal
    from PySide2.Qt import QPoint, QPolygon



class draw(QWidget):


    drawsig = pyqtSignal(bool)

    def __init__(self):
        super(draw, self).__init__()
        self.setWindowTitle("QPainter画图")
        self._painter = QPainter()
        self.scale = 1.0
        self.pixmap = QPixmap()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.WheelFocus)
        self.drawEnable = False
        self.points = []
        self.current_points = []
        self.drawsig.connect(self.setDrawEnable)


    def setDrawEnable(self, enable=False):
        self.drawEnable = enable
        self.update()

    def mouseMoveEvent(self, ev):
        if self.drawEnable:
            def in_end_range(curr, first):
                return first.x() - 5 <= curr.x() <= first.x() + 5 and first.y() - 5 <= curr.y() <= first.y() + 5

            if len(self.current_points) > 0 and in_end_range(ev.pos(), self.current_points[0]):
                self.current_points.append(self.current_points[0])
                self.points.append(self.current_points)
                self.current_points = []
            else:
                self.current_points.append(ev.pos())
        elif len(self.current_points) > 0:
            self.current_points.append(ev.pos())
            self.points.append(self.current_points)
            self.current_points = []

        self.update()

    def mousePressEvent(self, ev):
        if Qt.LeftButton & ev.button():
            self.drawsig.emit(True)
    def mouseReleaseEvent(self, ev):
        if Qt.LeftButton & ev.button():
            self.drawsig.emit(False)

    def paintEvent(self, ev):
        if len(self.points) <= 0 and len(self.current_points) <= 0 :  return
        p = self._painter
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.scale(self.scale, self.scale)
        p.setPen(QColor(0, 0, 0))
        for pts in self.points:
            p.drawPolyline(QPolygon(pts))
        if len(self.current_points) > 0:
            p.drawPolyline(QPolygon(self.current_points))
        p.end()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = draw()
    mainWin.show()
    sys.exit(app.exec_())

