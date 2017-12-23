#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月23日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: QChartToolTipTest
@description: 
'''
import random
import sys

from PyQt5.QtChart import QChartView, QChart, QLineSeries
from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QGraphicsWidget, QGraphicsGridLayout,\
    QGraphicsProxyWidget, QLabel, QWidget, QHBoxLayout,\
    QVBoxLayout


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

m_listCount = 3
m_valueMax = 10
m_valueCount = 7


def generateRandomData(listCount, valueMax, valueCount):
    random.seed()
    dataTable = []
    for i in range(listCount):
        dataList = []
        yValue = 0.0
        f_valueCount = float(valueCount)
        for j in range(valueCount):
            yValue += random.uniform(0, valueMax) / f_valueCount
            value = j + random.random() * m_valueMax / f_valueCount, yValue
            label = "Slice " + str(i) + ":" + str(j)
            dataList.append((value, label))
        dataTable.append(dataList)
    return dataTable


m_dataTable = generateRandomData(m_listCount, m_valueMax, m_valueCount)


class CircleWidget(QGraphicsProxyWidget):

    def __init__(self, color, *args, **kwargs):
        super(CircleWidget, self).__init__(*args, **kwargs)
        label = QLabel()
        label.setMinimumSize(12, 12)
        label.setMaximumSize(12, 12)
        label.setStyleSheet(
            "border:1px solid green;border-radius:6px;background: %s;" % color)
        self.setWidget(label)


class TextWidget(QGraphicsProxyWidget):

    def __init__(self, text, *args, **kwargs):
        super(TextWidget, self).__init__(*args, **kwargs)
        self.setWidget(QLabel(text, styleSheet="color:white;"))


class GraphicsWidget(QGraphicsWidget):

    def __init__(self, *args, **kwargs):
        super(GraphicsWidget, self).__init__(*args, **kwargs)
#         self.setFlags(self.ItemClipsChildrenToShape)
        self.setZValue(999)
        layout = QGraphicsGridLayout(self)
        for row in range(6):
            layout.addItem(CircleWidget("red"), row, 0)
            layout.addItem(TextWidget("red"), row, 1)
        self.hide()

    def show(self, pos):
        self.setGeometry(pos.x(), pos.y(), self.size().width(),
                         self.size().height())
        super(GraphicsWidget, self).show()


class ToolTipItem(QWidget):

    def __init__(self, color, text, parent=None):
        super(ToolTipItem, self).__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        clabel = QLabel(self)
        clabel.setMinimumSize(12, 12)
        clabel.setMaximumSize(12, 12)
        clabel.setStyleSheet("border-radius:6px;background: rgba(%s,%s,%s,%s);" % (
            color.red(), color.green(), color.blue(), color.alpha()))
        layout.addWidget(clabel)
        self.textLabel = QLabel(text, self, styleSheet="color:white;")
        layout.addWidget(self.textLabel)

    def setText(self, text):
        self.textLabel.setText(text)


class ToolTipWidget(QWidget):

    Cache = {}

    def __init__(self, *args, **kwargs):
        super(ToolTipWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            "ToolTipWidget{background: rgba(50,50,50,70);}")
        layout = QVBoxLayout(self)
        self.titleLabel = QLabel(self, styleSheet="color:white;")
        layout.addWidget(self.titleLabel)

    def updateUi(self, title, points):
        self.titleLabel.setText(title)
        for serie, point in points:
            if serie not in self.Cache:
                item = ToolTipItem(
                    serie.color(),
                    (serie.name() or "-") + ":" + str(point.y()), self)
                self.layout().addWidget(item)
                self.Cache[serie] = item
            else:
                self.Cache[serie].setText(
                    (serie.name() or "-") + ":" + str(point.y()))


class GraphicsProxyWidget(QGraphicsProxyWidget):

    def __init__(self, *args, **kwargs):
        super(GraphicsProxyWidget, self).__init__(*args, **kwargs)
        self.setZValue(999)
        self.tipWidget = ToolTipWidget()
        self.setWidget(self.tipWidget)
        self.hide()

    def show(self, title, points, pos):
        self.setGeometry(QRectF(pos, self.size()))
        self.tipWidget.updateUi(title, points)
        super(GraphicsProxyWidget, self).show()


class ChartView(QChartView):

    def __init__(self, *args, **kwargs):
        super(ChartView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.initChart()
#         self.toolTipWidget = GraphicsWidget(self._chart)
#         self.scene().addItem(self.toolTipWidget)

        self.toolTipWidget = GraphicsProxyWidget(self._chart)
        self.scene().addItem(self.toolTipWidget)

    def mouseMoveEvent(self, event):
        super(ChartView, self).mouseMoveEvent(event)
        # 获取x和y轴的最小最大值
        axisX, axisY = self._chart.axisX(), self._chart.axisY()
        min_x, max_x = axisX.min(), axisX.max()
        min_y, max_y = axisY.min(), axisY.max()
        step_x = (max_x - min_x) / (axisX.tickCount() - 1)
        step_y = (max_y - min_y) / (axisY.tickCount() - 1)
        # 把鼠标位置所在点转换为对应的xy值
        x = self._chart.mapToValue(event.pos()).x()
        y = self._chart.mapToValue(event.pos()).y()
#         print(x, y, step_x, step_y, event.pos())
        r_x = x / step_x
        r_y = y / step_y
        index = round(r_x) - 1  # 四舍五入
#         print(r_x, r_y, index, step_x, step_y)
        # 得到在坐标系中的所有series的类型和点
        points = [(serie, serie.at(index))
                  for serie in self._chart.series() if min_x <= x <= max_x and min_y <= y <= max_y]
        if points:
            self.toolTipWidget.show("", points, event.pos() + QPoint(20, 20))
        else:
            self.toolTipWidget.hide()

    def initChart(self):
        self._chart = QChart(title="Line Chart")
        for i, data_list in enumerate(m_dataTable):
            series = QLineSeries(self._chart)
            for value, _ in data_list:
                series.append(*value)
            series.setName("Series " + str(i))
            self._chart.addSeries(series)
        self._chart.createDefaultAxes()  # 创建默认的轴
#         self._chart = QChart()
#         self._chart.setTitle("Line Chart")
#         for i in range(1, 3):
#             series = QLineSeries(self._chart)
#             for j in range(6):
#                 series.append(j + i, j * 2 + 6)
#             series.setName("Line" + str(i))
#             self._chart.addSeries(series)
#         self._chart.createDefaultAxes()  # 创建默认轴
        self.setChart(self._chart)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = ChartView()
    view.show()
    sys.exit(app.exec_())
