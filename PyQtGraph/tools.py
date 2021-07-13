#!/usr/bin/env python
# encoding: utf-8
"""
Created on 2019年5月21日
@author: weike32
@site: https://pyqt.site ,https://github.com/weike32
@email: 394967319@qq.com
@file: CopyContent
@description: 工具类
"""
import pyqtgraph as pg
from pyqtgraph.exporters.ImageExporter import ImageExporter, Exporter
from pyqtgraph.parametertree import Parameter


# 不用修改源码，重加载，解决右键保存图片异常
def widthChanged(self):
    sr = self.getSourceRect()
    ar = float(sr.height()) / sr.width()
    self.params.param('height').setValue(int(self.params['width'] * ar), blockSignal=self.heightChanged)


def heightChanged(self):
    sr = self.getSourceRect()
    ar = float(sr.width()) / sr.height()
    self.params.param('width').setValue(int(self.params['height'] * ar), blockSignal=self.widthChanged)


def New__init__(self, item):
    Exporter.__init__(self, item)
    tr = self.getTargetRect()
    if isinstance(item, pg.Qt.QtGui.QGraphicsItem):
        scene = item.scene()
    else:
        scene = item
    bgbrush = scene.views()[0].backgroundBrush()
    bg = bgbrush.color()
    if bgbrush.style() == pg.Qt.QtCore.Qt.NoBrush:
        bg.setAlpha(0)

    self.params = Parameter(name='params', type='group', children=[
        {'name': 'width', 'type': 'int', 'value': int(tr.width()), 'limits': (0, None)},
        {'name': 'height', 'type': 'int', 'value': int(tr.height()), 'limits': (0, None)},
        {'name': 'antialias', 'type': 'bool', 'value': True},
        {'name': 'background', 'type': 'color', 'value': bg},
    ])
    self.params.param('width').sigValueChanged.connect(self.widthChanged)
    self.params.param('height').sigValueChanged.connect(self.heightChanged)


ImageExporter.heightChanged = heightChanged
ImageExporter.widthChanged = widthChanged
ImageExporter.__init__ = New__init__


# 解决自定义坐标轴密集显示
class MyStringAxis(pg.AxisItem):
    def __init__(self, xdict, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.xdict = xdict

    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            vs = v * scale
            if vs in self.xdict.keys():
                vstr = self.xdict[vs]
            else:
                vstr = ""
            strings.append(vstr)
        return strings


# 禁止鼠标事件
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
        pg.ViewBox.wheelEvent(self, ev, axis)
