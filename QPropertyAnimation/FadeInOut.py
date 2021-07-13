#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Created on 2018年6月14日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: FadeInOut
@description:
"""

try:
    from PyQt5.QtCore import QPropertyAnimation
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
except ImportError:
    from PySide2.QtCore import QPropertyAnimation
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton('退出', self, clicked=self.doClose))

        # 窗口透明度动画类
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(1000)  # 持续时间1秒

        # 执行淡入
        self.doShow()

    def doShow(self):
        try:
            # 尝试先取消动画完成后关闭窗口的信号
            self.animation.finished.disconnect(self.close)
        except:
            pass
        self.animation.stop()
        # 透明度范围从0逐渐增加到1
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def doClose(self):
        self.animation.stop()
        self.animation.finished.connect(self.close)  # 动画完成则关闭窗口
        # 透明度范围从1逐渐减少到0
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
