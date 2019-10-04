#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月19日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, http://coding.net/u/892768447, http://github.com/892768447
@email: 892768447@qq.com
@file: LineChart
@description: 
'''
import sys

from PyQt5.QtChart import QChartView, QLineSeries, QChart
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication

__version__ = "0.0.1"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chart = QChart()
    chart.setTitle("Line Chart 1")
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
