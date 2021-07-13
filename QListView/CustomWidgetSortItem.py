#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Created on 2018年8月4日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QListView.显示自定义Widget并排序
@description:
"""
import string
from random import choice, randint
from time import time

try:
    from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
    from PyQt5.QtGui import QStandardItem, QStandardItemModel
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListView, \
        QHBoxLayout, QLineEdit, QApplication
except ImportError:
    from PySide2.QtCore import QSortFilterProxyModel, Qt, QSize
    from PySide2.QtGui import QStandardItem, QStandardItemModel
    from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListView, \
        QHBoxLayout, QLineEdit, QApplication


def randomChar(y):
    # 返回随机字符串
    return ''.join(choice(string.ascii_letters) for _ in range(y))


class CustomWidget(QWidget):

    def __init__(self, text, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLineEdit(text, self))
        layout.addWidget(QPushButton('x', self))

    def sizeHint(self):
        # 决定item的高度
        return QSize(200, 40)


class SortFilterProxyModel(QSortFilterProxyModel):

    def lessThan(self, source_left, source_right):
        if not source_left.isValid() or not source_right.isValid():
            return False
        # 获取数据
        leftData = self.sourceModel().data(source_left)
        rightData = self.sourceModel().data(source_right)
        if self.sortOrder() == Qt.DescendingOrder:
            # 按照时间倒序排序
            leftData = leftData.split('-')[-1]
            rightData = rightData.split('-')[-1]
            return leftData < rightData
        #         elif self.sortOrder() == Qt.AscendingOrder:
        #             #按照名字升序排序
        #             leftData = leftData.split('-')[0]
        #             rightData = rightData.split('-')[0]
        #             return leftData < rightData
        return super(SortFilterProxyModel, self).lessThan(source_left, source_right)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QVBoxLayout(self)
        # 名字排序
        layout.addWidget(QPushButton('以名字升序', self, clicked=self.sortByName))
        # 时间倒序
        layout.addWidget(QPushButton('以时间倒序', self, clicked=self.sortByTime))
        # listview
        self.listView = QListView(self)
        layout.addWidget(self.listView)
        # 数据模型
        self.dmodel = QStandardItemModel(self.listView)
        # 排序代理模型
        self.fmodel = SortFilterProxyModel(self.listView)
        self.fmodel.setSourceModel(self.dmodel)
        self.listView.setModel(self.fmodel)

        # 模拟生成50条数据
        for _ in range(50):
            name = randomChar(5)
            times = time() + randint(0, 30)  # 当前时间随机+
            value = '{}-{}'.format(name, times)  # 内容用-分开
            item = QStandardItem(value)
            #             item.setData(value, Qt.UserRole + 2)
            self.dmodel.appendRow(item)
            # 索引
            index = self.fmodel.mapFromSource(item.index())
            # 自定义的widget
            widget = CustomWidget(value, self)
            item.setSizeHint(widget.sizeHint())
            self.listView.setIndexWidget(index, widget)

    def sortByTime(self):
        # 按照时间倒序排序
        self.fmodel.sort(0, Qt.DescendingOrder)

    def sortByName(self):
        # 按照名字升序排序
        self.fmodel.sort(0, Qt.AscendingOrder)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
