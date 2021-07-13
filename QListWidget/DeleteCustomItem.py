#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月4日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: 删除Item
@description: 
"""

try:
    from PyQt5.QtCore import QSize, pyqtSignal
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, \
        QListWidgetItem, QVBoxLayout, QListWidget, QApplication
except ImportError:
    from PySide2.QtCore import QSize, Signal as pyqtSignal
    from PySide2.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, \
        QListWidgetItem, QVBoxLayout, QListWidget, QApplication


class ItemWidget(QWidget):
    itemDeleted = pyqtSignal(QListWidgetItem)

    def __init__(self, text, item, *args, **kwargs):
        super(ItemWidget, self).__init__(*args, **kwargs)
        self._item = item  # 保留list item的对象引用
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLineEdit(text, self))
        layout.addWidget(QPushButton('x', self, clicked=self.doDeleteItem))

    def doDeleteItem(self):
        self.itemDeleted.emit(self._item)

    def sizeHint(self):
        # 决定item的高度
        return QSize(200, 40)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        # 列表
        self.listWidget = QListWidget(self)
        layout.addWidget(self.listWidget)

        # 清空按钮
        self.clearBtn = QPushButton('清空', self, clicked=self.doClearItem)
        layout.addWidget(self.clearBtn)

        # 添加测试数据
        self.testData()

    def doDeleteItem(self, item):
        # 根据item得到它对应的行数
        row = self.listWidget.indexFromItem(item).row()
        # 删除item
        item = self.listWidget.takeItem(row)
        # 删除widget
        self.listWidget.removeItemWidget(item)
        del item

    def doClearItem(self):
        # 清空所有Item
        for _ in range(self.listWidget.count()):
            # 删除item
            # 一直是0的原因是一直从第一行删,删掉第一行后第二行变成了第一行
            # 这个和删除list [] 里的数据是一个道理
            item = self.listWidget.takeItem(0)
            # 删除widget
            self.listWidget.removeItemWidget(item)
            del item

    def testData(self):
        # 生成测试数据
        for i in range(100):
            item = QListWidgetItem(self.listWidget)
            widget = ItemWidget('item: {}'.format(i), item, self.listWidget)
            # 绑定删除信号
            widget.itemDeleted.connect(self.doDeleteItem)
            self.listWidget.setItemWidget(item, widget)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
