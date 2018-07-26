#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年7月26日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: QGraphicsView练习.QGraphicsItem.Item移动
@description: 
"""
from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsView, QGraphicsScene,\
    QStyle


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class MoveableItem(QGraphicsRectItem):

    def __init__(self, *args, **kwargs):
        super(MoveableItem, self).__init__(*args, **kwargs)
        # 可移动,可选择,有焦点
        self.setFlags(self.ItemIsMovable |
                      self.ItemIsSelectable | self.ItemIsFocusable)
        # 设置接收悬停事件
        self.setAcceptHoverEvents(True)
        self.setBrush(QColor(247, 160, 57))  # 设置背景颜色

        # 是否在调整大小的状态
        self.isResizing = False

    def paint(self, painter, option, widget):
        super(MoveableItem, self).paint(painter, option, widget)
        # 当鼠标选中后在边缘绘制边框
        if option.state & QStyle.State_Selected:
            rect = self.boundingRect()
            painter.setRenderHint(QPainter.Antialiasing, True)  # 抗锯齿
            if option.state & QStyle.State_HasFocus:  # 有焦点
                painter.setPen(QPen(Qt.red, 2))  # 设置红色画笔
                painter.drawLines(  # 在左上、左下、右上、右下画8条小线段
                    QLineF(rect.x(), rect.y(), rect.x()+10, rect.y()),  # 左上顶点向右
                    QLineF(rect.x(), rect.y(), rect.x(), rect.y()+10),  # 左上顶点向下
                    
                    QLineF(rect.x(), rect.y()+rect.height(), rect.x()+10, rect.y()+rect.height()),  # 左下顶点向右
                    QLineF(rect.x(), rect.y()+rect.height(), rect.x(), rect.y()+rect.height() - 10),  # 左下顶点向上
                    
                    QLineF(rect.width(), rect.y(), rect.width() - 10, rect.y()),  # 右上顶点向左
                    QLineF(rect.width(), rect.y(), rect.width(), rect.y()+10),  # 右上顶点向下
                    
                    QLineF(rect.width(), rect.height(),
                           rect.width() - 10, rect.height()),  # 右下顶点向左
                    QLineF(rect.width(), rect.height(), rect.width(),
                           rect.height() - 10)  # 右下顶点向上
                )

    def hoverMoveEvent(self, event):
        super(MoveableItem, self).hoverMoveEvent(event)


class ImageWidget(QGraphicsView):

    def __init__(self, *args, **kwargs):
        super(ImageWidget, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        # 设置背景颜色
        self.setBackgroundBrush(QColor(31, 31, 47))
        # 去掉滚动条
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 设置变换中心为鼠标所在位置
        self.setTransformationAnchor(self.AnchorUnderMouse)
        # 不保证painter的状态
        self.setOptimizationFlags(self.DontSavePainterState)
        self.setViewportUpdateMode(self.SmartViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform)

        # 场景
        self._scene = QGraphicsScene(0, 0, self.width(), self.height())
        self.setScene(self._scene)

        self._scene.addItem(MoveableItem(100, 100, 200, 200))


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = ImageWidget()
    w.show()
    sys.exit(app.exec_())
