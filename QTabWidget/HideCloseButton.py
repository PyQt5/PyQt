#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2025/08/12
@author: Irony
@site: https://pyqt.site | https://github.com/PyQt5
@email: 892768447@qq.com
@file: HideCloseButton.py
@description:
"""

from PyQt5.QtWidgets import QApplication, QLabel, QTabBar, QTabWidget


class HideCloseButton(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.onCloseTab)

        # add tabs
        self.addTab(QLabel("Home", self), "Home")
        for i in range(10):
            title = "Tab {}".format(i)
            self.addTab(QLabel(title, self), title)

        # hide first tab's close button
        btn = self.tabBar().tabButton(0, QTabBar.RightSide)
        btn.close()
        self.tabBar().setTabButton(0, QTabBar.RightSide, None)

    def onCloseTab(self, index):
        w = self.widget(index)
        if w:
            w.close()
        self.removeTab(index)


if __name__ == "__main__":
    import cgitb
    import sys

    cgitb.enable(format="text")
    app = QApplication(sys.argv)
    w = HideCloseButton()
    w.show()
    sys.exit(app.exec_())
