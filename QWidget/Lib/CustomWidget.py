#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年12月10日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: CustomWidget
@description: 
"""

try:
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
except ImportError:
    from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel


class CustomWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("我是自定义CustomWidget", self))
