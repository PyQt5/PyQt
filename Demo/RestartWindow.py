#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年1月17日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: RestartWindow
@description: 窗口重启
"""

try:
    from PyQt5.QtCore import pyqtSignal
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, \
        QMessageBox, QApplication
except ImportError:
    from PySide2.QtCore import Signal as pyqtSignal
    from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, \
        QMessageBox, QApplication


class RestartWindow(QWidget):
    restarted = pyqtSignal(QWidget, str)
    _Self = None  # 很重要,保留窗口引用

    def __init__(self, path, *args, **kwargs):
        super(RestartWindow, self).__init__(*args, **kwargs)
        RestartWindow._Self = self
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("当前工作目录：" + path, self))
        self.dirEdit = QLineEdit(
            self, placeholderText="请输入要切换的目录", returnPressed=self.onChangeDir)
        layout.addWidget(self.dirEdit)
        layout.addWidget(QPushButton(
            "点我切换工作目录", self, clicked=self.onChangeDir))
        self.restarted.connect(RestartWindow.onRestart)

    def onChangeDir(self):
        path = self.dirEdit.text().strip()
        if path and QMessageBox.question(self, "提示", "确认要切换到{0}目录吗?".format(path)) == QMessageBox.Yes:
            self.hide()  # 先隐藏
            self.restarted.emit(self, path)
        else:
            self.dirEdit.setFocus()

    @classmethod
    def onRestart(cls, widget, path):
        w = RestartWindow(path)
        w.show()
        widget.close()
        widget.deleteLater()
        del widget


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = RestartWindow("test")
    w.show()
    sys.exit(app.exec_())
