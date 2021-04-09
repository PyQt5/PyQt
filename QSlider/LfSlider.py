#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021/4/9
@author: Irony
@site: https://github.com/PyQt5
@email: 892768447@qq.com
@file: LfSlider
@description: 降低值变化频率
"""
from datetime import datetime

from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import QSlider, QWidget, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QGroupBox


class LfSlider(QSlider):
    valueChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        delay = kwargs.pop('delay', 500)
        super(LfSlider, self).__init__(*args, **kwargs)
        self.lastValue = self.value()
        self.uTimer = QTimer(self)
        self.uTimer.timeout.connect(self.onValueChanged)
        self.uTimer.start(delay)

    def onValueChanged(self):
        if self.lastValue != self.value():
            self.lastValue = self.value()
            self.valueChanged.emit(self.lastValue)


class TestWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)

        # 左侧原始
        left_group = QGroupBox('原始QSlider', self)
        left_layout = QVBoxLayout(left_group)
        self.leftLabel = QPlainTextEdit(self)
        left_layout.addWidget(self.leftLabel)

        self.leftSlider = QSlider(Qt.Horizontal, self)
        self.leftSlider.valueChanged.connect(self.onLeftChanged)
        left_layout.addWidget(self.leftSlider)

        layout.addWidget(left_group)

        # 右侧低频率变化
        right_group = QGroupBox('LfSlider', self)
        right_layout = QVBoxLayout(right_group)
        self.rightLabel = QPlainTextEdit(self)
        right_layout.addWidget(self.rightLabel)

        self.rightSlider = LfSlider(Qt.Horizontal, self)
        self.rightSlider.valueChanged.connect(self.onRightChanged)
        right_layout.addWidget(self.rightSlider)

        layout.addWidget(right_group)

    def onLeftChanged(self, value):
        self.leftLabel.appendPlainText(datetime.now().strftime("[%H:%M:%S.%f]   ") + str(value))

    def onRightChanged(self, value):
        self.rightLabel.appendPlainText(datetime.now().strftime("[%H:%M:%S.%f]   ") + str(value))


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec_())
