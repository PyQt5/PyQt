#!/usr/bin/env python2
import os
import sys
import re

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.Qt import QDir

from PyQt5 import  QtGui, QtWidgets, QtCore, QtWinExtras
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

"""
Created on $date$ <br>
description: 树视图支持拖拽 并改变图标样式 <br>
author: 东love方 <br>

"""

class MyTreeWidget(QTreeWidget):

    def mouseMoveEvent_xxx(self, e):
        mimeData = QtCore.QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)

        # pixmap = QPixmap()
        # drag.setPixmap(pixmap)

        # drag.setHotSpot(e.pos())

        # QTreeWidget.mouseMoveEvent(self,e)
        drag.exec_(QtCore.Qt.MoveAction)

    def dropEvent(self, e):
        QTreeWidget.dropEvent(self, e)
        self.expandAll()
        e.accept()

    def startDrag(self, supportedActions):
        listsQModelIndex = self.selectedIndexes()
        if listsQModelIndex:
            dataQMimeData = self.model().mimeData(listsQModelIndex)
            if not dataQMimeData:
                return None
            dragQDrag = QDrag(self)
            dragQDrag.setPixmap(
                QPixmap(QDir.currentPath() + "/if_Cursor_drag_arrow_103039.png"))  # <- For put your
            # custom image here
            dragQDrag.setMimeData(dataQMimeData)
            defaultDropAction = QtCore.Qt.IgnoreAction
            if ((supportedActions & QtCore.Qt.CopyAction) and (self.dragDropMode() != QAbstractItemView.InternalMove)):
                defaultDropAction = QtCore.Qt.CopyAction
            dragQDrag.exec_(supportedActions, defaultDropAction)


class TheUI(QDialog):

    def __init__(self, args=None, parent=None):
        super(TheUI, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        treeWidget = MyTreeWidget()

        button = QPushButton('Add')
        self.layout.addWidget(treeWidget)
        self.layout.addWidget(button)
        treeWidget.setHeaderHidden(True)

        self.treeWidget = treeWidget
        self.button = button
        self.button.clicked.connect(lambda *x: self.addCmd())

        HEADERS = ("script", "chunksize", "mem")
        self.treeWidget.setHeaderLabels(HEADERS)
        self.treeWidget.setColumnCount(len(HEADERS))

        self.treeWidget.setColumnWidth(0, 160)
        self.treeWidget.header().show()

        self.treeWidget.setDragDropMode(QAbstractItemView.InternalMove)

        self.resize(500, 500)
        for i in range(6):
            item = self.addCmd(i)
            if i in (3, 4):
                self.addCmd('%s-1' % i, parent=item)

        self.treeWidget.expandAll()
        self.setStyleSheet("QTreeWidget::item{ height: 30px;  }")

    def addCmd(self, i, parent=None):
        'add a level to tree widget'

        root = self.treeWidget.invisibleRootItem()
        if not parent:
            parent = root
        item = QTreeWidgetItem(parent, ['script %s' % i, '1', '150'])
        return item

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = TheUI()
    gui.show()
    app.exec_()
