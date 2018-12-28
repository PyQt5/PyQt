#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月17日
@author: Irony."[讽刺]
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: RestartMainWindow
@description: 
'''
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,\
    QMessageBox


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class RestartMainWindow(QWidget):

    restarted = pyqtSignal(QWidget, str)
    _Self = None  # 很重要,保留窗口引用

    def __init__(self, path, *args, **kwargs):
        super(RestartMainWindow, self).__init__(*args, **kwargs)
        RestartMainWindow._Self = self
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("当前工作目录：" + path, self))
        self.dirEdit = QLineEdit(
            self, placeholderText="请输入要切换的目录", returnPressed=self.onChangeDir)
        layout.addWidget(self.dirEdit)
        layout.addWidget(QPushButton(
            "点我切换工作目录", self, clicked=self.onChangeDir))
        self.restarted.connect(RestartMainWindow.onRestart)

    def onChangeDir(self):
        path = self.dirEdit.text().strip()
        if path and QMessageBox.question(self, "提示", "确认要切换到{0}目录吗?".format(path)) == QMessageBox.Yes:
            self.hide()  # 先隐藏
            self.restarted.emit(self, path)
        else:
            self.dirEdit.setFocus()

    @classmethod
    def onRestart(cls, widget, path):
        w = RestartMainWindow(path)
        w.show()
        widget.close()
        widget.deleteLater()
        del widget


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = RestartMainWindow("test")
    w.show()
    sys.exit(app.exec_())
