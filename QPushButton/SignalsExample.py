#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月2日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QPushButton.SignalsExample
@description: 按钮信号例子
"""

try:
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QPlainTextEdit
except ImportError:
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QPlainTextEdit


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        btn1 = QPushButton('按钮点击信号', self)
        btn1.setObjectName('ClickBtn')
        btn1.clicked.connect(self.onClicked)
        layout.addWidget(btn1)

        btn2 = QPushButton('按钮按下信号', self)
        btn2.setObjectName('PressBtn')
        btn2.pressed.connect(self.onPressed)
        layout.addWidget(btn2)

        btn3 = QPushButton('按钮释放信号', self)
        btn3.setObjectName('ReleaseBtn')
        btn3.released.connect(self.onReleased)
        layout.addWidget(btn3)

        btn4 = QPushButton('按钮释放信号', self)
        btn4.setObjectName('ToggleBtn')
        btn4.setCheckable(True)
        btn4.toggled.connect(self.onToggled)
        layout.addWidget(btn4)

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

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
