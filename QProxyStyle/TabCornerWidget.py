#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021年06月23日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: TabCornerWidget
@description: 
"""

try:
    from PyQt5.QtCore import pyqtSignal, Qt
    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, \
        QTabWidget
except ImportError:
    from PySide2.QtCore import Signal as pyqtSignal, Qt
    from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, \
        QTabWidget

from QProxyStyle.Lib.TabCornerStyle import TabCornerStyle


class TabCornerWidget(QWidget):
    signalTabAdd = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(TabCornerWidget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.buttonAdd = QPushButton('+', self, toolTip='添加新标签页', clicked=self.signalTabAdd.emit)
        layout.addWidget(self.buttonAdd)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    def resizeEvent(self, event):
        super(TabCornerWidget, self).resizeEvent(event)
        # 更新按钮高度
        if hasattr(self, 'buttonAdd'):
            self.buttonAdd.setFixedSize(self.height(), self.height())


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle(TabCornerStyle())

    tab1 = QTabWidget()
    cor1 = TabCornerWidget(tab1)
    cor1.signalTabAdd.connect(lambda: tab1.addTab(QWidget(tab1), 'tab' + str(tab1.count() + 1)))
    tab1.setCornerWidget(cor1, Qt.TopRightCorner)
    tab1.show()

    tab2 = QTabWidget()
    tab2.setTabPosition(QTabWidget.South)  # tab 标签方向
    cor2 = TabCornerWidget(tab2)
    cor2.signalTabAdd.connect(lambda: tab2.addTab(QWidget(tab2), 'tab' + str(tab2.count() + 1)))
    tab2.setCornerWidget(cor2, Qt.BottomRightCorner)
    tab2.show()

    for i in range(10):
        tab1.addTab(QWidget(tab1), 'tab' + str(i + 1))
        tab2.addTab(QWidget(tab1), 'tab' + str(i + 1))

    sys.exit(app.exec_())
