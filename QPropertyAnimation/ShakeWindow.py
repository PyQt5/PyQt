#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年5月8日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ShakeWindow
@description: 抖动动画
"""

try:
    from PyQt5.QtCore import QPropertyAnimation, QPoint
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
except ImportError:
    from PySide2.QtCore import QPropertyAnimation, QPoint
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton('抖动', self, clicked=self.doShake))

    def doShake(self):
        self.doShakeWindow(self)

    # 下面这个方法可以做成这样的封装给任何控件
    def doShakeWindow(self, target):
        """窗口抖动动画
        :param target:        目标控件
        """
        if hasattr(target, '_shake_animation'):
            # 如果已经有该对象则跳过
            return

        animation = QPropertyAnimation(target, b'pos', target)
        target._shake_animation = animation
        animation.finished.connect(lambda: delattr(target, '_shake_animation'))

        pos = target.pos()
        x, y = pos.x(), pos.y()

        animation.setDuration(200)
        animation.setLoopCount(2)
        animation.setKeyValueAt(0, QPoint(x, y))
        animation.setKeyValueAt(0.09, QPoint(x + 2, y - 2))
        animation.setKeyValueAt(0.18, QPoint(x + 4, y - 4))
        animation.setKeyValueAt(0.27, QPoint(x + 2, y - 6))
        animation.setKeyValueAt(0.36, QPoint(x + 0, y - 8))
        animation.setKeyValueAt(0.45, QPoint(x - 2, y - 10))
        animation.setKeyValueAt(0.54, QPoint(x - 4, y - 8))
        animation.setKeyValueAt(0.63, QPoint(x - 6, y - 6))
        animation.setKeyValueAt(0.72, QPoint(x - 8, y - 4))
        animation.setKeyValueAt(0.81, QPoint(x - 6, y - 2))
        animation.setKeyValueAt(0.90, QPoint(x - 4, y - 0))
        animation.setKeyValueAt(0.99, QPoint(x - 2, y + 2))
        animation.setEndValue(QPoint(x, y))

        animation.start(animation.DeleteWhenStopped)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
