#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年12月23日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: AddQWidget
@description: 
"""
import sys

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, \
        QApplication, QGraphicsView, QGraphicsScene
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, \
        QApplication, QGraphicsView, QGraphicsScene


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
