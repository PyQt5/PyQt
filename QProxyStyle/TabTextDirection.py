#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年12月27日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: TestTabWidget
@description: 
"""
from PyQt5.QtWidgets import QTabWidget, QLabel, QWidget, QGridLayout

from Lib.TabBarStyle import TabBarStyle


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class TabWidget(QTabWidget):

    def __init__(self, *args, **kwargs):
        super(TabWidget, self).__init__(*args, **kwargs)
        for i in range(10):
            self.addTab(QLabel('Tab' + str(i)), str(i))


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QGridLayout(self)

        layout.addWidget(TabWidget(self, tabPosition=TabWidget.North), 0, 1)
        layout.addWidget(TabWidget(self, tabPosition=TabWidget.South), 2, 1)
        layout.addWidget(TabWidget(self, tabPosition=TabWidget.West), 1, 0)
        layout.addWidget(TabWidget(self, tabPosition=TabWidget.East), 1, 2)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyle(TabBarStyle())
    w = Window()
    w.show()
    sys.exit(app.exec_())
