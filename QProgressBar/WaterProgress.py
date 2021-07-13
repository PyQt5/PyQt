#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021/1/1
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: WaterProgress
@description: 
"""
import sys

try:
    from PyQt5.QtCore import QTimer
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
except ImportError:
    from PySide2.QtCore import QTimer
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout

from Lib.DWaterProgress import DWaterProgress


class WaterProgressWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(WaterProgressWindow, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        self.progress = DWaterProgress(self)
        self.progress.setFixedSize(100, 100)
        self.progress.setValue(0)
        self.progress.start()

        layout.addWidget(self.progress)

        self.timer = QTimer(self, timeout=self.updateProgress)
        self.timer.start(50)

    def updateProgress(self):
        value = self.progress.value()
        if value == 100:
            self.progress.setValue(0)
        else:
            self.progress.setValue(value + 1)


if __name__ == '__main__':
    import cgitb

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    w = WaterProgressWindow()
    w.show()
    sys.exit(app.exec_())
