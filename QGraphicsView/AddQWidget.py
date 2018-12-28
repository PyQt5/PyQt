#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年12月23日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: AddQWidget
@description: 
"""
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout,\
    QApplication, QGraphicsView, QGraphicsScene


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class ToolTipItem(QWidget):

    def __init__(self, color, text, parent=None):
        super(ToolTipItem, self).__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        clabel = QLabel(self)
        clabel.setMinimumSize(12, 12)
        clabel.setMaximumSize(12, 12)
        clabel.setStyleSheet("border-radius:6px;background: %s" % color)
        layout.addWidget(clabel)
        layout.addWidget(QLabel(text, self))


class ToolTipWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(ToolTipWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            "ToolTipWidget{background: rgba(50,50,50,70); border: none;};color:white")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("test", self))

        for color in ("red", "blue", "green", "yellow", "black"):
            layout.addWidget(ToolTipItem(color, color, self))


app = QApplication(sys.argv)
view = QGraphicsView()
view.resize(800, 600)
scene = QGraphicsScene(view)
view.setScene(scene)
view.show()

w = scene.addWidget(ToolTipWidget())
print(w)
sys.exit(app.exec_())
