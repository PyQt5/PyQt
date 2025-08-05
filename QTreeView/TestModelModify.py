#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2025/08/05
@author: Irony
@site: https://pyqt.site | https://github.com/PyQt5
@email: 892768447@qq.com
@file: TestModelModify.py
@description:
"""

import json
import sys

from Lib.qjsonmodel import QJsonItem, QJsonModel

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (
        QApplication,
        QFormLayout,
        QHBoxLayout,
        QLineEdit,
        QPlainTextEdit,
        QPushButton,
        QTreeView,
        QWidget,
    )
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import (
        QApplication,
        QFormLayout,
        QHBoxLayout,
        QLineEdit,
        QPlainTextEdit,
        QPushButton,
        QTreeView,
        QWidget,
    )


class TestWindow(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        self.treeView = QTreeView(self)
        self.widgetEdit = QWidget(self)
        layout.addWidget(self.treeView)
        layout.addWidget(self.widgetEdit)

        layout = QFormLayout(self.widgetEdit)
        layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.editPath = QLineEdit(f"address{QJsonItem.Sep}city", self.widgetEdit)
        self.editPath.setPlaceholderText(
            f"请输入查询内容，支持路径查询，比如：aaa{QJsonItem.Sep}bbb{QJsonItem.Sep}ccc"
        )
        layout.addRow("Path:", self.editPath)
        self.editValue = QLineEdit("SiChuan", self.widgetEdit)
        self.editValue.setPlaceholderText("请输入修改值，只支持路径匹配")
        layout.addRow("Value:", self.editValue)
        self.buttonQuery = QPushButton("查询", self.widgetEdit)
        self.buttonModify = QPushButton("修改", self.widgetEdit)
        self.buttonExport = QPushButton("获取Json", self.widgetEdit)
        layout.addRow("", self.buttonQuery)
        layout.addRow("", self.buttonModify)
        layout.addRow("", self.buttonExport)
        self.editText = QPlainTextEdit(self.widgetEdit)
        self.editText.setReadOnly(True)
        layout.addRow("", self.editText)
        self.buttonQuery.clicked.connect(self.doQuery)
        self.buttonModify.clicked.connect(self.doModify)
        self.buttonExport.clicked.connect(self.doExport)

        self.model = QJsonModel(self)
        self.model.itemChanged.connect(self.onItemChanged)
        self.treeView.setModel(self.model)

        self.setupModel()

    def doQuery(self):
        self.editText.clear()
        path = self.editPath.text().strip()
        if not path:
            return

        item = self.model.findPath(path)

        if item:
            self.editText.appendPlainText(
                str(
                    {
                        "path": item.path,
                        "text": item.text(),
                        "value": item.value.edit,
                    }
                )
            )

    def doModify(self):
        self.editText.clear()
        path = self.editPath.text().strip()
        value = self.editValue.text().strip()
        if not path or not value:
            return

        try:
            value = json.loads(value)
        except Exception:
            pass

        ret = self.model.updateValue(path, value)
        self.editText.setPlainText(f"change ret: {ret}")

    def doExport(self):
        self.editText.setPlainText(self.model.toJson(ensure_ascii=False, indent=4))

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

    def onItemChanged(self, item):
        self.doExport()


if __name__ == "__main__":
    import cgitb
    import sys

    cgitb.enable(format="text")
    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec_())
