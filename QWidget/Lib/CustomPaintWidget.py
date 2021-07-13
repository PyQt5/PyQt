#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年12月10日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: CustomPaintWidget
@description: 
"""

try:
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStyleOption, QStyle
except ImportError:
    from PySide2.QtGui import QPainter
    from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QStyleOption, QStyle


class CustomPaintWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(CustomPaintWidget, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("我是自定义CustomPaintWidget", self))

    def paintEvent(self, event):
        # 解决QSS问题
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
        super(CustomPaintWidget, self).paintEvent(event)
