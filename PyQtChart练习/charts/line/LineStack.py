#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月28日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: charts.line.LineStack
@description: like http://echarts.baidu.com/demo.html#line-stack
'''

import sys

from PyQt5.QtChart import QChartView, QChart, QLineSeries
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsLineItem


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class ChartView(QChartView):

    def __init__(self, *args, **kwargs):
        super(ChartView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.initChart()

        # line
        self.lineItem = QGraphicsLineItem(self._chart)
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        self.lineItem.setPen(pen)
        self.lineItem.setZValue(998)
        self.lineItem.hide()

    def mouseMoveEvent(self, event):
        super(ChartView, self).mouseMoveEvent(event)
        # 获取x和y轴的最小最大值
        axisX, axisY = self._chart.axisX(), self._chart.axisY()
        min_x, max_x = axisX.min(), axisX.max()
        min_y, max_y = axisY.min(), axisY.max()
        # 坐标系中左上角顶点
        point_top = self._chart.mapToPosition(QPointF(min_x, max_y))
        # 坐标原点坐标
        point_bottom = self._chart.mapToPosition(QPointF(min_x, min_y))
        step_x = (max_x - min_x) / (axisX.tickCount() - 1)
        # 把鼠标位置所在点转换为对应的xy值
        x = self._chart.mapToValue(event.pos()).x()
        index = round((x - min_x) / step_x)
        pos_x = self._chart.mapToPosition(
            QPointF(index * step_x + min_x, min_y))
        self.lineItem.setLine(pos_x.x(), point_top.y(),
                              pos_x.x(), point_bottom.y())
        self.lineItem.show()

    def initChart(self):
        self._chart = QChart(title="折线图堆叠")
        self._chart.setAcceptHoverEvents(True)
        dataTable = [
            ["邮件营销", [120, 132, 101, 134, 90, 230, 210]],
            ["联盟广告", [220, 182, 191, 234, 290, 330, 310]],
            ["视频广告", [150, 232, 201, 154, 190, 330, 410]],
            ["直接访问", [320, 332, 301, 334, 390, 330, 320]],
            ["搜索引擎", [820, 932, 901, 934, 1290, 1330, 1320]]
        ]
        for series_name, data_list in dataTable:
            series = QLineSeries(self._chart)
            for j, v in enumerate(data_list):
                series.append(j, v)
            series.setName(series_name)
            series.setPointsVisible(True)  # 显示圆点
            self._chart.addSeries(series)
        self._chart.createDefaultAxes()  # 创建默认的轴
        axisX = self._chart.axisX()  # x轴
        axisX.setTickCount(7)  # x轴设置7个刻度
        axisX.setGridLineVisible(False)  # 隐藏从x轴往上的线条
        axisY = self._chart.axisY()
        axisY.setTickCount(7)  # y轴设置7个刻度
        axisY.setRange(0, 1500)  # 设置y轴范围
        self.setChart(self._chart)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = ChartView()
    view.show()
    sys.exit(app.exec_())
