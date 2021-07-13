#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年12月10日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: test
@description: 
"""

import sys

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QWidget, QApplication, QHBoxLayout

from Lib.CustomPaintWidget import CustomPaintWidget  # @UnresolvedImport
from Lib.CustomWidget import CustomWidget  # @UnresolvedImport


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(CustomPaintWidget(self))
        layout.addWidget(CustomWidget(self))
        # 注意
        wc = CustomWidget(self)
        wc.setAttribute(Qt.WA_StyledBackground)  # 很重要
        layout.addWidget(wc)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet('''
CustomPaintWidget {
    min-width: 100px;
    min-height: 100px;
    border: 1px solid green;
    border-radius: 20px;
    background: green;
}
CustomWidget {
    min-width: 200px;
    min-height: 200px;
    max-width: 200px;
    max-height: 200px;
    border: 1px solid orange;
    border-radius: 100px;
    background: orange;
}
    ''')
    w = Window()
    w.show()
    sys.exit(app.exec_())
