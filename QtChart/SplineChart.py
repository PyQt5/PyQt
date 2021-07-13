#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019/10/2
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: SplineChart
@description: 样条图表
"""

try:
    from PyQt5.QtChart import QChartView, QChart, QSplineSeries
    from PyQt5.QtCore import QPointF
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from PySide2.QtCore import QPointF
    from PySide2.QtGui import QPainter
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCharts import QtCharts

    QChartView = QtCharts.QChartView
    QChart = QtCharts.QChart
    QSplineSeries = QtCharts.QSplineSeries


class Window(QChartView):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(400, 300)
        # 抗锯齿
        self.setRenderHint(QPainter.Antialiasing)

        # 图表
        chart = QChart()
        self.setChart(chart)
        # 设置标题
        chart.setTitle('Simple splinechart example')
        # 添加Series
        self.getSeries(chart)
        # 创建默认xy轴
        chart.createDefaultAxes()
        chart.legend().setVisible(False)

    def getSeries(self, chart):
        # 第一组
        series = QSplineSeries(chart)
        series << QPointF(1, 5) << QPointF(3, 7) << QPointF(7, 6) << QPointF(9, 7) \
        << QPointF(12, 6) << QPointF(16, 7) << QPointF(18, 5)
        chart.addSeries(series)

        # 第二组
        series = QSplineSeries(chart)
        series << QPointF(1, 3) << QPointF(3, 4) << QPointF(7, 3) << QPointF(8, 2) \
        << QPointF(12, 3) << QPointF(16, 4) << QPointF(18, 3)
        chart.addSeries(series)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
