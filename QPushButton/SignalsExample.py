#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月2日
@author: Irony
@site: https://pyqt5.com https://github.com/PyQt5
@email: 892768447@qq.com
@file: QPushButton.SignalsExample
@description: 按钮信号例子
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QPlainTextEdit


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"
__Version__ = "Version 1.0"


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        btn1 = QPushButton('按钮点击信号', self)
        btn1.setObjectName('ClickBtn')
        btn1.clicked.connect(self.onClicked)

        layout.addWidget(btn1)
        layout.addWidget(QPushButton(
            '按钮按下信号', self, objectName='PressBtn', pressed=self.onPressed))
        layout.addWidget(QPushButton(
            '按钮释放信号', self, objectName='ReleaseBtn', released=self.onReleased))
        layout.addWidget(QPushButton(
            '按钮选中信号', self, checkable=True, objectName='ToggleBtn', toggled=self.onToggled))

        self.resultView = QPlainTextEdit(self)
        self.resultView.setReadOnly(True)
        layout.addWidget(self.resultView)

    def onClicked(self):
        self.resultView.appendPlainText(
            '按钮{0}被点击'.format(self.sender().objectName()))

    def onPressed(self):
        self.resultView.appendPlainText(
            '按钮{0}被按下'.format(self.sender().objectName()))

    def onReleased(self):
        self.resultView.appendPlainText(
            '按钮{0}被释放'.format(self.sender().objectName()))

    def onToggled(self, checked):
        self.resultView.appendPlainText(
            '按钮{0}被选中：{1}'.format(self.sender().objectName(), checked))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
