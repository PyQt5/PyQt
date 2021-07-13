#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年1月20日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ScrollBar
@description: 
"""
import chardet

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QTextEdit, QApplication
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QTextEdit, QApplication


class Window(QTextEdit):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.resize(800, 600)
        # 设置横向纵向滚动条总是显示
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        with open("Data/ScrollBar.qss", "rb") as fp:
            content = fp.read()
            encoding = chardet.detect(content) or {}
            content = content.decode(encoding.get("encoding") or "utf-8")
        self.setText(content)
        # 设置样式
        self.setStyleSheet(content)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("滚动条样式")
    app.setApplicationDisplayName("滚动条样式")
    window = Window()
    window.show()
    sys.exit(app.exec_())
