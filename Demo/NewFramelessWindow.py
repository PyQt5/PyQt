#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年4月30日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: NewFramelessWindow
@description:
"""

from Lib.ui_frameless import Ui_FormFrameless
from PyQt5.QtCore import QTimer, Qt, QEvent, QObject
from PyQt5.QtGui import QWindow, QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox


class FramelessObject(QObject):

    @staticmethod
    def _get_edges(pos):
        """根据坐标获取方向
        :param pos: QPoint
        :return: Qt::Edges
        """
        edge = 0
        x, y = pos.x(), pos.y()
        widget = QApplication.instance().activeWindow()
        if not widget:
            return edge
        left, top, right, bottom = widget.layout().getContentsMargins()

        if y <= top:
            edge |= Qt.TopEdge
        if x <= left:
            edge |= Qt.LeftEdge
        if x >= widget.width() - right:
            edge |= Qt.RightEdge
        if y >= widget.height() - bottom:
            edge |= Qt.BottomEdge

        return edge

    @staticmethod
    def _adjust_cursor(edges):
        """调整鼠标样式
        :param edges: int or None
        """
        # print('edges', edges)
        widget = QApplication.instance().activeWindow()
        if not widget:
            return
        if edges == Qt.LeftEdge | Qt.TopEdge or edges == Qt.RightEdge | Qt.BottomEdge:
            widget.setCursor(Qt.SizeFDiagCursor)
        elif edges == Qt.RightEdge | Qt.TopEdge or edges == Qt.LeftEdge | Qt.BottomEdge:
            widget.setCursor(Qt.SizeBDiagCursor)
        elif edges == Qt.LeftEdge or edges == Qt.RightEdge:
            widget.setCursor(Qt.SizeHorCursor)
        elif edges == Qt.TopEdge or edges == Qt.BottomEdge:
            widget.setCursor(Qt.SizeVerCursor)
        else:
            widget.setCursor(Qt.ArrowCursor)

    def eventFilter(self, obj, event):
        # 鼠标移动改变光标
        if event.type() == QEvent.MouseMove:
            widget = QApplication.instance().activeWindow()
            if widget and event.buttons() == Qt.NoButton and not (
                    widget.isMaximized() or widget.isFullScreen()):
                # 鼠标移动变更光标样式
                # print('MouseMove', event.pos())
                self._adjust_cursor(self._get_edges(event.pos()))

        if event.type() == QEvent.MouseButtonPress and obj.objectName() == 'FramelessWindow':
            # 鼠标按下
            edges = self._get_edges(event.pos())
            # 标题栏高度
            try:
                height = obj.titleHeight()
            except AttributeError:
                height = 36
            # 优先判断边缘
            widget = QApplication.instance().activeWindow()
            if edges != 0 and not (widget.isMaximized() or widget.isFullScreen()):
                # 按下窗口边缘边距位置
                self._adjust_cursor(edges)
                # 交给系统去调整大小
                print('startSystemResize')
                obj.windowHandle().startSystemResize(edges)
            elif event.y() <= height:
                # 标题栏交给系统去移动
                print('startSystemMove')
                obj.windowHandle().startSystemMove()
        elif event.type() == QEvent.MouseButtonRelease:
            # 鼠标释放
            self._adjust_cursor(None)
        return False


class FramelessWindow(QWidget, Ui_FormFrameless):

    def __init__(self, *args, **kwargs):
        super(FramelessWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setObjectName('FramelessWindow')  # 过滤器中的名字一致
        # 无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        # 隐藏还原按钮
        self.buttonNormal.setVisible(False)
        # 标题栏按钮信号
        self.buttonMinimum.clicked.connect(self.showMinimized)
        self.buttonMaximum.clicked.connect(self.showMaximized)
        self.buttonNormal.clicked.connect(self.showNormal)
        self.buttonClose.clicked.connect(self.close)
        self.setStyleSheet('#widgetTitleBar{background: rgb(232, 232, 232);}')

    def titleHeight(self):
        """标题栏高度
        :return: int
        """
        return self.widgetTitleBar.height()

    def mouseDoubleClickEvent(self, event):
        """双击最大化还原
        :param event: QMouseEvent
        """
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        event.accept()

    def changeEvent(self, event):
        """窗口状态改变
        :param event:
        """
        super(FramelessWindow, self).changeEvent(event)
        # 窗口状态改变时修改标题栏控制按钮
        visible = self.isMaximized()
        self.buttonMaximum.setVisible(not visible)
        self.buttonNormal.setVisible(visible)
        if visible:
            self.layout().setContentsMargins(0, 0, 0, 0)
        else:
            # TODO 与UI文件中的布局边距一致
            self.layout().setContentsMargins(3, 3, 3, 3)

    def paintEvent(self, event):
        # 透明背景但是需要留下一个透明度用于鼠标捕获
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255, 1))


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    if not hasattr(QWindow, 'startSystemMove'):
        QWindow.startSystemResize()
        # 不支持
        QMessageBox.critical(None, '错误', '当前Qt版本不支持该例子')
        QTimer.singleShot(100, app.quit)
    else:
        # 安装全局事件过滤器
        fo = FramelessObject()
        app.installEventFilter(fo)
        w = FramelessWindow()
        w.show()
    sys.exit(app.exec_())
