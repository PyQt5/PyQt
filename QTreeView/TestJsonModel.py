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

from Lib.qjsonmodel import QJsonItem, QJsonModel

try:
    from PyQt5.QtCore import QModelIndex, QSortFilterProxyModel, Qt
    from PyQt5.QtWidgets import (
        QAction,
        QApplication,
        QCheckBox,
        QGridLayout,
        QLineEdit,
        QPlainTextEdit,
        QTreeView,
        QWidget,
    )
except ImportError:
    from PySide2.QtCore import QModelIndex, QSortFilterProxyModel, Qt
    from PySide2.QtWidgets import (
        QAction,
        QApplication,
        QCheckBox,
        QGridLayout,
        QLineEdit,
        QPlainTextEdit,
        QTreeView,
        QWidget,
    )


class TestWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QGridLayout(self)
        self.filterPath = QCheckBox("Path Filter?", self)
        self.filterEdit = QLineEdit(self)
        self.treeView = QTreeView(self)
        self.widgetEdit = QPlainTextEdit(self)
        layout.addWidget(self.filterPath, 0, 0, 1, 1)
        layout.addWidget(self.filterEdit, 0, 1, 1, 1)
        layout.addWidget(self.treeView, 1, 0, 1, 2)
        layout.addWidget(self.widgetEdit, 0, 2, 2, 1)

        self.filterPath.toggled.connect(self.onFilterPathToggled)
        self.filterEdit.setPlaceholderText("过滤条件")
        self.filterEdit.textChanged.connect(self.onFilterTextChanged)

        self.model = QJsonModel(self)
        self.model.itemChanged.connect(self.onItemChanged)
        self.model.rowsRemoved.connect(self.onRowsRemoved)
        self.treeView.clicked.connect(self.onItemChanged)
        action = QAction("Delete", self.treeView)
        action.triggered.connect(self.deleteItem)
        self.treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.treeView.addAction(action)

        # setup model data
        self.setupModel()

        # filter model
        self.fmodel = QSortFilterProxyModel(self)
        self.fmodel.setSourceModel(self.model)
        self.fmodel.setRecursiveFilteringEnabled(True)
        self.treeView.setModel(self.fmodel)
        self.treeView.expandAll()

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
        if item.keyItem:
            keyInfo = f"row={item.keyItem.row()}, col={item.keyItem.column()}, text={item.keyItem.text()}"
        print(
            f"row={item.row()}, col={item.column()}, text={item.text()}, value={str(item.data(Qt.EditRole))}, key=({keyInfo})\n\trowCount={item.rowCount()}\n\tpath={item.path}"
        )

    def onFilterPathToggled(self, checked):
        if checked:
            self.fmodel.setFilterRole(QJsonItem.PathRole)
        else:
            self.fmodel.setFilterRole(Qt.DisplayRole)

    def onFilterTextChanged(self, text):
        self.fmodel.setFilterFixedString(text)


if __name__ == "__main__":
    import cgitb
    import sys

    cgitb.enable(format="text")
    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec_())
