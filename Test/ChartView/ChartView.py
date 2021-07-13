#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年12月18日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ChartView
@description: 
"""
import json
import os

import chardet
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QCategoryAxis
from PyQt5.QtCore import QMargins, Qt, QEasingCurve
from PyQt5.QtGui import QColor, QBrush, QFont, QPainter, QPen, QPixmap

# QEasingCurve 类型枚举
EasingCurve = dict(
    [(c, getattr(QEasingCurve, n)) for n, c in QEasingCurve.__dict__.items()
     if isinstance(c, QEasingCurve.Type)])

# 动画 类型枚举
AnimationOptions = {
    0: QChart.NoAnimation,
    1: QChart.GridAxisAnimations,
    2: QChart.SeriesAnimations,
    3: QChart.AllAnimations
}


class ChartView(QChartView):

    def __init__(self, file, parent=None):
        super(ChartView, self).__init__(parent)
        self._chart = QChart()
        self._chart.setAcceptHoverEvents(True)
        self.setChart(self._chart)
        self.initUi(file)

    def initUi(self, file):
        if isinstance(file, dict):
            return self.__analysis(file)
        if isinstance(file, str):
            if not os.path.isfile(file):
                return self.__analysis(json.loads(file))
            with open(file, "rb") as fp:
                data = fp.read()
                encoding = chardet.detect(data) or {}
                data = data.decode(encoding.get("encoding") or "utf-8")
            self.__analysis(json.loads(data))

    #     def onSeriesHoverd(self, point, state):
    #         print(point, state)

    def mouseMoveEvent(self, event):
        super(ChartView, self).mouseMoveEvent(event)
        # 获取x和y轴的最小最大值
        axisX, axisY = self._chart.axisX(), self._chart.axisY()
        min_x, max_x = axisX.min(), axisX.max()
        min_y, max_y = axisY.min(), axisY.max()
        # 把鼠标位置所在点转换为对应的xy值
        x = self._chart.mapToValue(event.pos()).x()
        y = self._chart.mapToValue(event.pos()).y()
        index = round(x)  # 四舍五入
        print(x, y, index)
        # 得到在坐标系中的所有series的类型和点
        points = [(s.type(), s.at(index))
                  for s in self._chart.series() if min_x <= x <= max_x and min_y <= y <= max_y]
        print(points)

    def __getColor(self, color=None, default=Qt.white):
        '''
        :param color: int|str|[r,g,b]|[r,g,b,a]
        '''
        if not color:
            return QColor(default)
        if isinstance(color, QBrush):
            return color
        # 比如[r,g,b]或[r,g,b,a]
        if isinstance(color, list) and 3 <= len(color) <= 4:
            return QColor(*color)
        else:
            return QColor(color)

    def __getPen(self, pen=None, default=QPen(
        Qt.white, 1, Qt.SolidLine,
        Qt.SquareCap, Qt.BevelJoin)):
        '''
        :param pen: pen json
        '''
        if not pen or not isinstance(pen, dict):
            return default
        return QPen(
            self.__getColor(pen.get("color", None) or default.color()),
            pen.get("width", 1) or 1,
            pen.get("style", 0) or 0,
            pen.get("capStyle", 16) or 16,
            pen.get("joinStyle", 64) or 64
        )

    def __getAlignment(self, alignment):
        '''
        :param alignment: left|top|right|bottom
        '''
        try:
            return getattr(Qt, "Align" + alignment.capitalize())
        except:
            return Qt.AlignTop

    #         if alignment == "left":
    #             return Qt.AlignLeft
    #         if alignment == "right":
    #             return Qt.AlignRight
    #         if alignment == "bottom":
    #             return Qt.AlignBottom
    #         return Qt.AlignTop

    def __setTitle(self, title=None):
        '''
        :param title: title json
        '''
        if not title or not isinstance(title, dict):
            return
        # 设置标题
        self._chart.setTitle(title.get("text", "") or "")
        # 设置标题颜色
        self._chart.setTitleBrush(self.__getColor(
            title.get("color", self._chart.titleBrush()) or self._chart.titleBrush()))
        # 设置标题字体
        font = QFont(title.get("font", "") or self._chart.titleFont())
        pointSize = title.get("pointSize", -1) or -1
        if pointSize > 0:
            font.setPointSize(pointSize)
        font.setWeight(title.get("weight", -1) or -1)
        font.setItalic(title.get("italic", False) or False)
        self._chart.setTitleFont(font)

    def __setAnimation(self, animation=None):
        '''
        :param value: animation json
        '''
        if not animation or not isinstance(animation, dict):
            return
        # 动画持续时间
        self._chart.setAnimationDuration(
            animation.get("duration", 1000) or 1000)
        # 设置动画曲线
        self._chart.setAnimationEasingCurve(EasingCurve.get(
            animation.get("curve", 10) or 10, None) or QEasingCurve.OutQuart)
        # 设置开启何种动画
        self._chart.setAnimationOptions(AnimationOptions.get(
            animation.get("options", 0) or 0, None) or QChart.NoAnimation)

    def __setBackground(self, background=None):
        '''
        :param background:background json
        '''
        if not background or not isinstance(background, dict):
            return
        # 设置是否背景可用
        self._chart.setBackgroundVisible(
            background.get("visible", True) or True)
        # 设置背景矩形的圆角
        self._chart.setBackgroundRoundness(
            background.get("radius", 0) or 0)
        # 设置下拉阴影
        self._chart.setDropShadowEnabled(
            background.get("dropShadow", True) or True)
        # 设置pen
        self._chart.setBackgroundPen(self.__getPen(
            background.get("pen", None), self._chart.backgroundPen()))
        # 设置背景
        image = background.get("image", None)
        color = background.get("color", None)
        if image:
            self._chart.setBackgroundBrush(QBrush(QPixmap(image)))
        elif color:
            self._chart.setBackgroundBrush(self.__getColor(
                color, self._chart.backgroundBrush()))

    def __setMargins(self, margins=None):
        '''
        :param margins: margins json
        '''
        if not margins or not isinstance(margins, dict):
            return
        left = margins.get("left", 20) or 20
        top = margins.get("top", 20) or 20
        right = margins.get("right", 20) or 20
        bottom = margins.get("bottom", 20) or 20
        self._chart.setMargins(QMargins(left, top, right, bottom))

    def __setLegend(self, legend=None):
        '''
        :param legend: legend json
        '''
        if not legend or not isinstance(legend, dict):
            return
        _legend = self._chart.legend()
        _legend.setAlignment(self.__getAlignment(
            legend.get("alignment", None)))
        _legend.setShowToolTips(legend.get("showToolTips", True) or True)

    def __getSerie(self, serie=None):
        if not serie or not isinstance(serie, dict):
            return None
        types = serie.get("type", "") or ""
        data = serie.get("data", []) or []
        if not data or not isinstance(data, list):
            return None
        if types == "line":
            _series = QLineSeries(self._chart)
        else:
            return None
        # 设置series名字
        _series.setName(serie.get("name", "") or "")
        # 添加数据到series中
        for index, value in enumerate(data):
            # 保证vlaue必须是数字
            _series.append(index, value if type(value) in (int, float) else 0)
        return _series

    def __setSeries(self, series=None):
        if not series or not isinstance(series, list):
            return
        for serie in series:
            _serie = self.__getSerie(serie)
            if _serie:
                #                 _serie.hovered.connect(self.onSeriesHoverd)
                self._chart.addSeries(_serie)
        # 创建默认的xy轴
        self._chart.createDefaultAxes()

    def __setAxisX(self, axisx=None):
        if not axisx or not isinstance(axisx, dict):
            return
        series = self._chart.series()
        if not series:
            return
        types = axisx.get("type", None)
        data = axisx.get("data", []) or []
        if not data or not isinstance(data, list):
            return None
        minx = self._chart.axisX().min()
        maxx = self._chart.axisX().max()
        if types == "category":
            xaxis = QCategoryAxis(
                self._chart, labelsPosition=QCategoryAxis.AxisLabelsPositionOnValue)
            # 隐藏网格
            xaxis.setGridLineVisible(False)
            # 刻度条数
            tickc_d = len(data)
            tickc = tickc_d if tickc_d > 1 else self._chart.axisX().tickCount()
            xaxis.setTickCount(tickc)
            # 强制x轴刻度与新刻度条数一致
            self._chart.axisX().setTickCount(tickc)
            step = (maxx - minx) / (tickc - 1)
            for i in range(min(tickc_d, tickc)):
                xaxis.append(data[i], minx + i * step)
            self._chart.setAxisX(xaxis, series[-1])

    def __analysis(self, datas):
        '''
        analysis json data
        :param datas: json data
        '''
        # 标题
        self.__setTitle(datas.get("title", None))
        # 抗锯齿
        if (datas.get("antialiasing", False) or False):
            self.setRenderHint(QPainter.Antialiasing)
        # 主题
        self._chart.setTheme(datas.get("theme", 0) or 0)
        # 动画
        self.__setAnimation(datas.get("animation", None))
        # 背景设置
        self.__setBackground(datas.get("background", None))
        # 边距设置
        self.__setMargins(datas.get("margins", None))
        # 设置图例
        self.__setLegend(datas.get("legend", None))
        # 设置series
        self.__setSeries(datas.get("series", None))
        # 自定义的x轴
        self.__setAxisX(datas.get("axisx", None))
        # 自定义的y轴
