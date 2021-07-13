#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/7/3
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ThumbnailToolBar
@description: 
"""

import cgitb
import sys

try:
    from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QStyle, QVBoxLayout
    from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton
except ImportError:
    from PySide2.QtWidgets import QWidget, QApplication, QLabel, QStyle, QVBoxLayout
    from PySide2.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.countPrev = 0
        self.countNext = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.labelPrev = QLabel(self)
        self.labelControl = QLabel('暂停播放', self)
        self.labelNext = QLabel(self)
        layout.addWidget(self.labelPrev)
        layout.addWidget(self.labelControl)
        layout.addWidget(self.labelNext)

        # 任务栏缩略图工具条
        self.toolBar = QWinThumbnailToolBar(self)
        # 上一首，播放/暂停，下一首按钮
        self.toolBtnPrev = QWinThumbnailToolButton(self.toolBar)
        self.toolBtnPrev.setToolTip('上一首')
        self.toolBtnPrev.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.toolBtnPrev.clicked.connect(self.set_prev)
        self.toolBar.addButton(self.toolBtnPrev)

        self.toolBtnControl = QWinThumbnailToolButton(self.toolBar)
        self.toolBtnControl.setToolTip('播放')
        self.toolBtnControl.setProperty('status', 0)
        self.toolBtnControl.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.toolBtnControl.clicked.connect(self.set_control)
        self.toolBar.addButton(self.toolBtnControl)

        self.toolBtnNext = QWinThumbnailToolButton(self.toolBar)
        self.toolBtnNext.setToolTip('下一首')
        self.toolBtnNext.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.toolBtnNext.clicked.connect(self.set_next)
        self.toolBar.addButton(self.toolBtnNext)

    def set_prev(self):
        self.countPrev += 1
        self.labelPrev.setText('点击上一首按钮: %d 次' % self.countPrev)

    def set_next(self):
        self.countNext += 1
        self.labelNext.setText('点击下一首按钮: %d 次' % self.countNext)

    def set_control(self):
        if self.toolBtnControl.property('status') == 0:
            self.labelControl.setText('正在播放')
            self.toolBtnControl.setProperty('status', 1)
            self.toolBtnControl.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.labelControl.setText('暂停播放')
            self.toolBtnControl.setProperty('status', 0)
            self.toolBtnControl.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def showEvent(self, event):
        super(Window, self).showEvent(event)
        if not self.toolBar.window():
            # 必须等窗口显示后设置才有效，或者通过软件流程在适当的时候设置也可以
            self.toolBar.setWindow(self.windowHandle())


if __name__ == '__main__':
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
