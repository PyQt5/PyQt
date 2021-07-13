#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月1日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: WeltHideWindow
@description: 简单的窗口贴边隐藏
"""

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication


class WeltHideWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(WeltHideWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.resize(800, 600)
        self._width = QApplication.desktop().availableGeometry(self).width()
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton("关闭窗口", self, clicked=self.close))

    def mousePressEvent(self, event):
        '''鼠标按下事件，需要记录下坐标self._pos 和 是否可移动self._canMove'''
        super(WeltHideWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._pos = event.globalPos() - self.pos()
            # 当窗口最大化或者全屏时不可移动
            self._canMove = not self.isMaximized() or not self.isFullScreen()

    def mouseMoveEvent(self, event):
        '''鼠标移动事件，动态调整窗口位置'''
        super(WeltHideWindow, self).mouseMoveEvent(event)
        if event.buttons() == Qt.LeftButton and self._canMove:
            self.move(event.globalPos() - self._pos)

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件，这个时候需要判断窗口的左边是否符合贴到左边，顶部，右边一半'''
        super(WeltHideWindow, self).mouseReleaseEvent(event)
        self._canMove = False
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x < 0:
            # 隐藏到左边
            return self.move(1 - self.width(), y)
        if y < 0:
            # 隐藏到顶部
            return self.move(x, 1 - self.height())
        if x > self._width - self.width() / 2:  # 窗口进入右边一半距离
            # 隐藏到右边
            return self.move(self._width - 1, y)

    def enterEvent(self, event):
        '''鼠标进入窗口事件，用于弹出显示窗口'''
        super(WeltHideWindow, self).enterEvent(event)
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x < 0:
            return self.move(0, y)
        if y < 0:
            return self.move(x, 0)
        if x > self._width - self.width() / 2:
            return self.move(self._width - self.width(), y)

    def leaveEvent(self, event):
        '''鼠标离开事件，如果原先窗口已经隐藏，并暂时显示，此时离开后需要再次隐藏'''
        super(WeltHideWindow, self).leaveEvent(event)
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x == 0:
            return self.move(1 - self.width(), y)
        if y == 0:
            return self.move(x, 1 - self.height())
        if x == self._width - self.width():
            return self.move(self._width - 1, y)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = WeltHideWindow()
    w.show()
    sys.exit(app.exec_())
