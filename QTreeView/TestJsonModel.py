#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2025/08/05
@author: Irony
@site: https://pyqt.site | https://github.com/PyQt5
@email: 892768447@qq.com
@file: TestJsonModel.py
@description:
"""

import sys

from Lib.qjsonmodel import QJsonModel

try:
    from PyQt5.QtCore import QModelIndex, Qt
    from PyQt5.QtWidgets import (
        QAction,
        QApplication,
        QHBoxLayout,
        QPlainTextEdit,
        QTreeView,
        QWidget,
    )
except ImportError:
    from PySide2.QtCore import QModelIndex, Qt
    from PySide2.QtWidgets import (
        QAction,
        QApplication,
        QHBoxLayout,
        QPlainTextEdit,
        QTreeView,
        QWidget,
    )


class TestWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QHBoxLayout(self)
        self.treeView = QTreeView(self)
        self.widgetEdit = QPlainTextEdit(self)
        layout.addWidget(self.treeView)
        layout.addWidget(self.widgetEdit)

        self.model = QJsonModel(self)
        self.model.itemChanged.connect(self.onItemChanged)
        self.model.rowsRemoved.connect(self.onRowsRemoved)
        self.treeView.setModel(self.model)
        self.treeView.clicked.connect(self.onItemChanged)
        action = QAction("Delete", self.treeView)
        action.triggered.connect(self.deleteItem)
        self.treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.treeView.addAction(action)

        self.setupModel()

    def setupModel(self):
        data = {
            "name": "Irony",
            "age": 33,
            "address": {
                "country": "China",
                "city": "Chengdu",
            },
            "phone": [
                {"type": "home", "number": "123456789"},
                {"type": "fax", "number": "6987654321"},
            ],
            "marriage": False,
            "salary": 6666.6,
            "skills": [
                "C++",
                "Python",
                "Java",
                "JavaScript",
                "Shell",
                "Android",
            ],
            "others": [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ],
        }
        self.model.blockSignals(True)
        self.model.loadData(data)
        self.model.blockSignals(False)

        self.treeView.expandAll()
        self.doExport()

    def doExport(self):
        self.widgetEdit.setPlainText(self.model.toJson(ensure_ascii=False, indent=4))

    def deleteItem(self, _):
        indexes = self.treeView.selectedIndexes()
        if not indexes:
            return

        index = indexes[0]
        print(index.row(), index.column(), index.parent())
        self.model.removeRow(index.row(), index.parent())

    def onRowsRemoved(self, parent, first, last):
        print("onRowsRemoved", parent, first, last)
        self.doExport()

    def onItemChanged(self, item):
        if self.sender() == self.model:
            self.doExport()

        if isinstance(item, QModelIndex):
            item = self.model.itemFromIndex(item)

        if not item:
            return
        keyInfo = ""
        if item.key:
            keyInfo = (
                f"row={item.key.row()}, col={item.key.column()}, text={item.key.text()}"
            )
        print(
            f"row={item.row()}, col={item.column()}, text={item.text()}, value={str(item.data(Qt.EditRole))}, key=({keyInfo})\n\trowCount={item.rowCount()}\n\tpath={item.path}"
        )


if __name__ == "__main__":
    import cgitb
    import sys

    cgitb.enable(format="text")
    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec_())
