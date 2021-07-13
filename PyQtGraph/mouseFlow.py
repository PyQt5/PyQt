#!/usr/bin/env python
# encoding: utf-8
"""
Created on 2019年5月2日
@author: weike32
@site: https://pyqt.site ,https://github.com/weike32
@email: 394967319@qq.com
@file: CopyContent
@description: 查阅了很多博客，如果有异，可以联系作者邮箱。本Demo仅作学习参考用，保有后续相关权益。
"""
import sys

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(726, 595)
        self.graphicsView = pg.PlotWidget(Form)
        self.graphicsView.setGeometry(QtCore.QRect(75, 131, 621, 441))
        self.graphicsView.setObjectName("graphicsView")


class MyWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        x = np.linspace(-100, 100, 1000)
        data = np.sin(x) / x
        self.graphicsView.plot(data, pen=(255, 255, 255, 200))
        self.label = pg.TextItem(text="横坐标：{}".format(0))
        self.graphicsView.addItem(self.label)
        self.setMouseTracking(True)
        self.graphicsView.scene().sigMouseMoved.connect(self.onMouseMoved)

    def onMouseMoved(self, evt):
        if self.graphicsView.plotItem.vb.mapSceneToView(evt):
            point = self.graphicsView.plotItem.vb.mapSceneToView(evt)
            self.label.setHtml("<p style='color:white'>横坐标：{0}</p>".format(point.x()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
