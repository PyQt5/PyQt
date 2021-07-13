#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年4月6日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: DreamTree
@description: 
"""

import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout


# from PyQt5.QtWebKit import QWebSettings


# 要实现透明的webview,需要先用一个QWidget作为父控件


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置父控件Widget背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去掉边框
        palette = self.palette()
        palette.setBrush(QPalette.Base, Qt.transparent)  # 父控件背景透明
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        #         QWebSettings.globalSettings().setAttribute(
        #             QWebSettings.DeveloperExtrasEnabled, True)# web开发者工具

        self.webView = QWebView(self)  # 网页控件
        layout.addWidget(self.webView)
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)  # 去掉右键菜单
        self.mainFrame = self.webView.page().mainFrame()

        self.mainFrame.setScrollBarPolicy(
            Qt.Vertical, Qt.ScrollBarAlwaysOff)  # 去掉滑动条
        self.mainFrame.setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)

        # 最大化
        rect = app.desktop().availableGeometry()
        self.resize(rect.size())
        self.webView.resize(rect.size())

    def load(self):
        self.webView.load(QUrl('qrc:/tree.html'))  # 加载网页


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.load()
    sys.exit(app.exec_())
