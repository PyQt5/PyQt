#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月3日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QListWidget.SignalsExample
@description: 
"""

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QColor
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QPlainTextEdit, \
        QListWidgetItem, QAbstractItemView, QListView, QApplication
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QColor
    from PySide2.QtWidgets import QWidget, QHBoxLayout, QListWidget, QPlainTextEdit, \
        QListWidgetItem, QAbstractItemView, QListView, QApplication


def formatColor(text, color):
    return '<font color={0}>{1}</font>'.format(color.name(), text)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)

        self.listWidget = QListWidget(self)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.setMovement(QListView.Free)
        self.listWidget.setMouseTracking(True)  # 用于itemEntered信号

        self.resultView = QPlainTextEdit(self)
        self.resultView.setReadOnly(True)

        layout.addWidget(self.listWidget)
        layout.addWidget(self.resultView)

        self.initData()
        self.initSignals()

    def initData(self):
        # 初始化模拟数据
        for i in range(100):
            item = QListWidgetItem('Item {0}'.format(i), self.listWidget)
            if i % 3 == 0:
                item.setFlags(item.flags() | Qt.ItemIsEditable)

    def initSignals(self):
        # 初始化信号
        self.listWidget.currentItemChanged.connect(self.onCurrentItemChanged)
        self.listWidget.currentRowChanged.connect(self.onCurrentRowChanged)
        self.listWidget.currentTextChanged.connect(self.onCurrentTextChanged)
        self.listWidget.itemActivated.connect(self.onItemActivated)
        self.listWidget.itemChanged.connect(self.onItemChanged)
        self.listWidget.itemClicked.connect(self.onItemClicked)
        self.listWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.listWidget.itemEntered.connect(self.onItemEntered)
        self.listWidget.itemPressed.connect(self.onItemPressed)
        self.listWidget.itemSelectionChanged.connect(
            self.onItemSelectionChanged)

    def onCurrentItemChanged(self, current, previous):
        current = current.text() if current else ''
        previous = previous.text() if previous else ''
        self.resultView.appendHtml(
            '{0}: [{1}] -> [{2}]'.format(
                formatColor('currentItemChanged', QColor(Qt.red)),
                current, previous))

    def onCurrentRowChanged(self, currentRow):
        self.resultView.appendHtml(
            '{0}: {1}'.format(
                formatColor('currentRowChanged', QColor(Qt.green)),
                currentRow))

    def onCurrentTextChanged(self, currentText):
        self.resultView.appendHtml(
            '{0}: {1}'.format(
                formatColor('currentTextChanged', QColor(Qt.yellow)), currentText))

    def onItemActivated(self, item):
        self.resultView.appendHtml(
            '{0}: {1}'.format(
                formatColor('itemActivated', QColor(Qt.blue)), item.text()))

    def onItemChanged(self, item):
        self.resultView.appendHtml(
            '{0}: {1}'.format(
                formatColor('itemChanged', QColor(Qt.cyan)), item.text()))

    def onItemClicked(self, item):
        self.resultView.appendHtml(
            '{0}: {1}'.format(formatColor('itemClicked', QColor(Qt.magenta)), item.text()))

    def onItemDoubleClicked(self, item):
        self.resultView.appendHtml(
            '{0}: {1}'.format(formatColor('itemDoubleClicked', QColor(Qt.darkGreen)), item.text()))

    def onItemEntered(self, item):
        self.resultView.appendHtml(
            '{0}: {1}'.format(formatColor('itemEntered', QColor(Qt.darkCyan)), item.text()))

    def onItemPressed(self, item):
        print(item)
        self.resultView.appendHtml(
            '{0}: {1}'.format(formatColor('itemPressed', QColor(Qt.darkYellow)), item.text()))

    def onItemSelectionChanged(self):
        self.resultView.appendPlainText('itemSelectionChanged')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
