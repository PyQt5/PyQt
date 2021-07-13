#!/usr/bin/env python
# encoding: utf-8
"""
Created on 2019年5月21日
@author: weike32
@site: https://pyqt.site ,https://github.com/weike32
@email: 394967319@qq.com
@file: CopyContent
@description: 禁止右键，添加滑动窗口，点击按钮生成图片，自定义Y轴坐标，背景颜色调整
"""
import sys

import pyqtgraph as pg
from PyQt5.QtGui import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QScrollArea, QVBoxLayout

from PyQtGraph.Data.graphTest import graph_Form


class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.RectMode = 3
        self.setMouseMode(self.RectMode)

    def mouseClickEvent(self, ev):
        if ev.button() == pg.QtCore.Qt.RightButton:
            self.autoRange()

    def mouseDragEvent(self, ev):
        pg.ViewBox.mouseDragEvent(self, ev)

    def wheelEvent(self, ev, axis=None):
        # pg.ViewBox.wheelEvent(self, ev, axis)
        ev.ignore()


class graphAnalysis(QDialog, graph_Form):
    def __init__(self):
        super(graphAnalysis, self).__init__()
        self.setupUi(self)
        self.pushButton_7.clicked.connect(self.test)
        self.tabWidget.clear()

    def test(self):
        tab1 = QWidget()
        scrollArea = QScrollArea(tab1)
        scrollArea.setMinimumSize(984, 550)
        scrollArea.setWidgetResizable(True)
        labelsContainer = QWidget()
        labelsContainer.setMinimumSize(0, 1500)
        scrollArea.setWidget(labelsContainer)
        layout = QVBoxLayout(labelsContainer)
        time = ['2019-04-20 08:09:00', '2019-04-20 08:09:00', '2019-04-20 08:09:00', '2019-04-20 08:09:00']
        value = [1.2, 2, 1, 4]
        xdict = dict(enumerate(time))
        ticks = [list(zip(range(4), tuple(time)))]
        vb = CustomViewBox()
        plt = pg.PlotWidget(title="标题这里填写", viewBox=vb)
        plt.setBackground(background=None)
        plt.plot(list(xdict.keys()), value)
        plt.getPlotItem().getAxis("bottom").setTicks(ticks)
        temp = QWidget()
        temp.setMinimumSize(900, 300)
        temp.setMaximumSize(900, 300)
        layout1 = QVBoxLayout(temp)
        layout1.addWidget(plt)
        layout.addWidget(temp)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                 QSizePolicy.Expanding)
        layout.addItem(spacerItem)
        self.tabWidget.addTab(tab1, '这里tabWidget修改标签')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = graphAnalysis()
    w.show()
    sys.exit(app.exec_())
