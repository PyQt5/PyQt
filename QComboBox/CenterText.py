#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2022/09/03
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: CenterText.py
@description: 文字居中对齐
"""

import sys

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication, QStyle, QVBoxLayout, QWidget
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QStyle, QVBoxLayout, QWidget

from Lib.CtComboBox import CtComboBox


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        c1 = CtComboBox(self)
        c1.addItems(['item-%s' % i for i in range(10)])
        layout.addWidget(c1)

        # 可编辑
        c2 = CtComboBox(self)
        c2.setEditable(True)
        c2.lineEdit().setAlignment(Qt.AlignCenter)
        c2.addItems(['item-%s' % i for i in range(10)])
        layout.addWidget(c2)

        # 带图标
        c3 = CtComboBox(self)
        for i in range(10):
            c3.addItem(c3.style().standardIcon(QStyle.SP_ComputerIcon),
                       'item-%s' % i)
        layout.addWidget(c3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
