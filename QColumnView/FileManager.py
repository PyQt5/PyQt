#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2025/04/08
@author: Irony
@site: https://pyqt.site | https://github.com/PyQt5
@email: 892768447@qq.com
@file: FileManager.py
@description:
"""

try:
    from PyQt5.QtWidgets import (
        QApplication,
        QColumnView,
        QFileSystemModel,
        QGridLayout,
        QMessageBox,
        QPushButton,
        QSizePolicy,
        QSpacerItem,
        QWidget,
    )
except Exception:
    from PySide2.QtWidgets import (
        QApplication,
        QColumnView,
        QFileSystemModel,
        QGridLayout,
        QMessageBox,
        QPushButton,
        QSizePolicy,
        QSpacerItem,
        QWidget,
    )


class FileManager(QWidget):  # type: ignore
    def __init__(self, *args, **kwargs):
        super(FileManager, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self._view = QColumnView(self)
        self._btn = QPushButton("确定", self)
        layout = QGridLayout(self)
        layout.addWidget(self._view, 0, 0, 1, 2)
        layout.addItem(
            QSpacerItem(
                40,
                20,
                QSizePolicy.Expanding,
                QSizePolicy.Minimum,
            ),
            1,
            0,
        )
        layout.addWidget(self._btn, 1, 1, 1, 1)
        layout.setRowStretch(1, 0)
        self._model = QFileSystemModel(self)
        self._model.setRootPath("")  # 设置根路径
        self._view.setModel(self._model)  # type: ignore
        self._btn.clicked.connect(self.onAccept)  # type: ignore

    def onAccept(self):
        path = self._model.filePath(self._view.currentIndex())
        print("path", path)
        if path:
            QMessageBox.information(self, "提示", "路径：%s" % path)


if __name__ == "__main__":
    import cgitb
    import sys

    cgitb.enable(format="text")
    app = QApplication(sys.argv)
    w = FileManager()
    w.show()
    sys.exit(app.exec_())
