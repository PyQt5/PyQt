#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年12月19日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: LineChart
@description: 
"""
import sys

try:
    from PyQt5.QtChart import QChartView, QLineSeries, QChart
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from PySide2.QtGui import QPainter
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCharts import QtCharts

    QChartView = QtCharts.QChartView
    QChart = QtCharts.QChart
    QLineSeries = QtCharts.QLineSeries

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chart = QChart()
    chart.setTitle('Line Chart 1')
    series = QLineSeries(chart)
    series.append(0, 6)
    series.append(2, 4)
    chart.addSeries(series)
    chart.createDefaultAxes()  # 创建默认轴

    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())
