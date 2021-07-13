#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年4月6日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: CopyContent
@description: 
"""

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QStandardItemModel, QStandardItem
    from PyQt5.QtWidgets import QTableView, QApplication, QAction, QMessageBox
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QStandardItemModel, QStandardItem
    from PySide2.QtWidgets import QTableView, QApplication, QAction, QMessageBox


class TableView(QTableView):

    def __init__(self, parent=None):
        super(TableView, self).__init__(parent)
        self.resize(800, 600)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)  # 右键菜单
        self.setEditTriggers(self.NoEditTriggers)  # 禁止编辑
        self.doubleClicked.connect(self.onDoubleClick)
        self.addAction(QAction("复制", self, triggered=self.copyData))
        self.myModel = QStandardItemModel()  # model
        self.initHeader()  # 初始化表头
        self.setModel(self.myModel)
        self.initData()  # 初始化模拟数据

    def onDoubleClick(self, index):
        print(index.row(), index.column(), index.data())

    def keyPressEvent(self, event):
        super(TableView, self).keyPressEvent(event)
        # Ctrl + C
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            self.copyData()

    def copyData(self):
        count = len(self.selectedIndexes())
        if count == 0:
            return
        if count == 1:  # 只复制了一个
            QApplication.clipboard().setText(
                self.selectedIndexes()[0].data())  # 复制到剪贴板中
            QMessageBox.information(self, "提示", "已复制一个数据")
            return
        rows = set()
        cols = set()
        for index in self.selectedIndexes():  # 得到所有选择的
            rows.add(index.row())
            cols.add(index.column())
            # print(index.row(),index.column(),index.data())
        if len(rows) == 1:  # 一行
            QApplication.clipboard().setText("\t".join(
                [index.data() for index in self.selectedIndexes()]))  # 复制
            QMessageBox.information(self, "提示", "已复制一行数据")
            return
        if len(cols) == 1:  # 一列
            QApplication.clipboard().setText("\r\n".join(
                [index.data() for index in self.selectedIndexes()]))  # 复制
            QMessageBox.information(self, "提示", "已复制一列数据")
            return
        mirow, marow = min(rows), max(rows)  # 最(少/多)行
        micol, macol = min(cols), max(cols)  # 最(少/多)列
        print(mirow, marow, micol, macol)
        arrays = [
            [
                "" for _ in range(macol - micol + 1)
            ] for _ in range(marow - mirow + 1)
        ]  # 创建二维数组(并排除前面的空行和空列)
        print(arrays)
        # 填充数据
        for index in self.selectedIndexes():  # 遍历所有选择的
            arrays[index.row() - mirow][index.column() - micol] = index.data()
        print(arrays)
        data = ""  # 最后的结果
        for row in arrays:
            data += "\t".join(row) + "\r\n"
        print(data)
        QApplication.clipboard().setText(data)  # 复制到剪贴板中
        QMessageBox.information(self, "提示", "已复制")

    def initHeader(self):
        for i in range(5):
            self.myModel.setHorizontalHeaderItem(
                i, QStandardItem("表头" + str(i + 1)))

    def initData(self):
        for row in range(100):
            for col in range(5):
                self.myModel.setItem(
                    row, col, QStandardItem("row: {row},col: {col}".format(row=row + 1, col=col + 1)))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("TableView")
    w = TableView()
    w.show()
    sys.exit(app.exec_())
