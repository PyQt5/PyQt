#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021/4/13
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ScreenNotify
@description: 屏幕、分辨率、DPI变化通知
"""
import sys

try:
    from PyQt5.QtCore import QTimer, QRect
    from PyQt5.QtWidgets import QApplication, QPlainTextEdit
except ImportError:
    from PySide2.QtCore import QTimer, QRect
    from PySide2.QtWidgets import QApplication, QPlainTextEdit


class Window(QPlainTextEdit):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.appendPlainText('修改分辨率后查看')
        # 记录最后一次的值（减少槽调用）
        self.m_rect = QRect()
        # 使用定时器来延迟触发最后一次变化
        self.m_timer = QTimer(self, timeout=self.onSolutionChanged)
        self.m_timer.setSingleShot(True)  # **重要** 保证多次信号尽量少的调用函数

        # 主要是多屏幕->无屏幕->有屏幕
        QApplication.instance().primaryScreenChanged.connect(lambda _: self.m_timer.start(1000))
        # 其它信号最终基本上都会调用该信号
        QApplication.instance().primaryScreen().virtualGeometryChanged.connect(
            lambda _: self.m_timer.start(1000))
        # DPI变化
        QApplication.instance().primaryScreen().logicalDotsPerInchChanged.connect(
            lambda _: self.m_timer.start(1000))

    def onSolutionChanged(self):
        # 获取主屏幕
        screen = QApplication.instance().primaryScreen()
        if self.m_rect == screen.availableVirtualGeometry():
            return
        self.m_rect = screen.availableVirtualGeometry()
        # 所有屏幕可用大小
        self.appendPlainText('\navailableVirtualGeometry: {0}'.format(str(screen.availableVirtualGeometry())))
        # 获取所有屏幕
        screens = QApplication.instance().screens()
        for screen in screens:
            self.appendPlainText(
                'screen: {0}, geometry({1}), availableGeometry({2}), logicalDotsPerInch({3}), '
                'physicalDotsPerInch({4}), refreshRate({5})'.format(
                    screen.name(), screen.geometry(), screen.availableGeometry(), screen.logicalDotsPerInch(),
                    screen.physicalDotsPerInch(), screen.refreshRate()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
