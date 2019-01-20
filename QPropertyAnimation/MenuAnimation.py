#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年8月22日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: MenuAnimation
@description: 
"""
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtWidgets import QWidget, QMenu, QApplication


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.initMenu()
        self.initAnimation()

    def contextMenuEvent(self, event):
        pos = event.globalPos()
        size = self._contextMenu.sizeHint()
        x, y, w, h = pos.x(), pos.y(), size.width(), size.height()
        self._animation.stop()
        self._animation.setStartValue(QRect(x, y, 0, 0))
        self._animation.setEndValue(QRect(x, y, w, h))
        self._animation.start()
        self._contextMenu.exec_(event.globalPos())

    def hello(self):
        QApplication.instance().aboutQt()

    def initAnimation(self):
        # 按钮动画
        self._animation = QPropertyAnimation(
            self._contextMenu, b'geometry', self,
            easingCurve=QEasingCurve.Linear, duration=300)
        # easingCurve 修改该变量可以实现不同的效果

    def initMenu(self):
        self._contextMenu = QMenu(self)
        self._contextMenu.addAction('菜单1', self.hello)
        self._contextMenu.addAction('菜单2', self.hello)
        self._contextMenu.addAction('菜单3', self.hello)
        self._contextMenu.addAction('菜单4', self.hello)
        self._contextMenu.addAction('菜单5', self.hello)
        self._contextMenu.addAction('菜单6', self.hello)


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
