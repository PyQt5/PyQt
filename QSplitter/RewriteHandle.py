#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月21日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: Splitter
@description: 
"""
import sys

try:
    from PyQt5.QtCore import Qt, QPointF, pyqtSignal
    from PyQt5.QtGui import QPainter, QPolygonF
    from PyQt5.QtWidgets import QTextEdit, QListWidget, \
        QTreeWidget, QSplitter, QApplication, QMainWindow, QSplitterHandle
except ImportError:
    from PySide2.QtCore import Qt, QPointF, Signal as pyqtSignal
    from PySide2.QtGui import QPainter, QPolygonF
    from PySide2.QtWidgets import QTextEdit, QListWidget, \
        QTreeWidget, QSplitter, QApplication, QMainWindow, QSplitterHandle


class SplitterHandle(QSplitterHandle):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(SplitterHandle, self).__init__(*args, **kwargs)
        # 如果不设置这个，则鼠标只能在按下后移动才能响应mouseMoveEvent
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        super(SplitterHandle, self).mousePressEvent(event)
        if event.pos().y() <= 24:
            # 发送点击信号
            self.clicked.emit()

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        # 当y坐标小于24时,也就是顶部的矩形框高度
        if event.pos().y() <= 24:
            # 取消鼠标样式
            self.unsetCursor()
            event.accept()
        else:
            # 设置默认的鼠标样式并可以移动
            self.setCursor(Qt.SplitHCursor if self.orientation()
                                              == Qt.Horizontal else Qt.SplitVCursor)
            super(SplitterHandle, self).mouseMoveEvent(event)

    def paintEvent(self, event):
        # 绘制默认的样式
        super(SplitterHandle, self).paintEvent(event)
        # 绘制顶部扩展按钮
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.red)
        # 画矩形
        painter.drawRect(0, 0, self.width(), 24)
        # 画三角形
        painter.setBrush(Qt.red)
        painter.drawPolygon(QPolygonF([
            QPointF(0, (24 - 8) / 2),
            QPointF(self.width() - 2, 24 / 2),
            QPointF(0, (24 + 8) / 2)
        ]))


class Splitter(QSplitter):

    def onClicked(self):
        print('clicked')

    def createHandle(self):
        if self.count() == 1:
            # 这里表示第一个分割条
            handle = SplitterHandle(self.orientation(), self)
            handle.clicked.connect(self.onClicked)
            return handle
        return super(Splitter, self).createHandle()


class SplitterWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SplitterWindow, self).__init__(parent)
        self.resize(400, 400)
        self.setWindowTitle('PyQt Qsplitter')
        textedit = QTextEdit('QTextEdit', self)
        listwidget = QListWidget(self)
        listwidget.addItem("This is  a \nListWidget!")
        treewidget = QTreeWidget()
        treewidget.setHeaderLabels(['This', 'is', 'a', 'TreeWidgets!'])

        splitter = Splitter(self)
        splitter.setHandleWidth(8)
        splitter.addWidget(textedit)
        splitter.addWidget(listwidget)
        splitter.addWidget(treewidget)
        # Qt.Vertical 垂直   Qt.Horizontal 水平
        splitter.setOrientation(Qt.Horizontal)
        self.setCentralWidget(splitter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = SplitterWindow()
    main.show()
    sys.exit(app.exec_())
