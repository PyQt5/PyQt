#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年5月5日
@author: Yimelia
@site: https://github.com/yimelia
@file: DynamicSpline
@description: This example shows how to draw dynamic data. https://doc.qt.io/qt-5/qtcharts-dynamicspline-example.html
"""
import sys

try:
    from PyQt5.QtChart import QChartView, QChart, QSplineSeries, QValueAxis
    from PyQt5.QtCore import Qt, QTimer, QRandomGenerator
    from PyQt5.QtGui import QPainter, QPen
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from PySide2.QtCore import Qt, QTimer, QRandomGenerator
    from PySide2.QtGui import QPainter, QPen
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCharts import QtCharts

    QChartView = QtCharts.QChartView
    QChart = QtCharts.QChart
    QSplineSeries = QtCharts.QSplineSeries
    QValueAxis = QtCharts.QValueAxis


class DynamicSpline(QChart):
    def __init__(self):
        super().__init__()
        self.m_step = 0
        self.m_x = 5
        self.m_y = 1
        # 初始化图像
        self.series = QSplineSeries(self)
        green_pen = QPen(Qt.red)
        green_pen.setWidth(3)
        self.series.setPen(green_pen)
        self.axisX = QValueAxis()
        self.axisY = QValueAxis()
        self.series.append(self.m_x, self.m_y)

        self.addSeries(self.series)
        self.addAxis(self.axisX, Qt.AlignBottom)
        self.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)
        self.axisX.setTickCount(5)
        self.axisX.setRange(0, 10)
        self.axisY.setRange(-5, 10)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.handleTimeout)
        self.timer.start()

    def handleTimeout(self):
        x = self.plotArea().width() / self.axisX.tickCount()
        y = (self.axisX.max() - self.axisX.min()) / self.axisX.tickCount()
        self.m_x += y
        # 在PyQt5.11.3及以上版本中，QRandomGenerator.global()被重命名为global_()
        self.m_y = QRandomGenerator.global_().bounded(5) - 2.5
        self.series.append(self.m_x, self.m_y)
        self.scroll(x, 0)
        if self.m_x >= 100:
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chart = DynamicSpline()
    chart.setTitle("Dynamic spline chart")
    chart.legend().hide()
    chart.setAnimationOptions(QChart.AllAnimations)

    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
    view.resize(400, 300)
    view.show()
    sys.exit(app.exec_())
