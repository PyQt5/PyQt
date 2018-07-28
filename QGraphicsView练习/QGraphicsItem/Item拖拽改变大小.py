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
from PyQt5.QtCore import Qt, QLineF, QRectF
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
        self.setPos(0, 0)
        # 可移动,可选择,有焦点,发送大小位置改变事件
        self.setFlags(self.ItemIsMovable | self.ItemIsSelectable |
                      self.ItemIsFocusable | self.ItemSendsGeometryChanges)
        # 设置接收悬停事件
        self.setAcceptHoverEvents(True)
        self.setBrush(QColor(247, 160, 57))  # 设置背景颜色

        # 是否在调整大小的状态
        self.isResizing = False
        self.prePos = None

    def paint(self, painter, option, widget):
        super(MoveableItem, self).paint(painter, option, widget)
        # 当鼠标选中后在边缘绘制边框
        if option.state & QStyle.State_Selected:
            rect = self.boundingRect()
            painter.setRenderHint(QPainter.Antialiasing, True)  # 抗锯齿
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            if option.state & QStyle.State_HasFocus:  # 有焦点
                painter.setPen(QPen(Qt.red, 3))  # 设置红色画笔
                painter.drawLines(  # 在左上、左下、右上、右下画8条小线段
                    QLineF(x, y, x + 10, y),  # 左上顶点向右
                    QLineF(x, y, x, y + 10),  # 左上顶点向下

                    QLineF(x, y + h, x + 10, y + h),  # 左下顶点向右
                    QLineF(x, y + h, x, y + h - 10),  # 左下顶点向上

                    QLineF(x + w, y, x + w - 10, y),  # 右上顶点向左
                    QLineF(x + w, y, x + w, y + 10),  # 右上顶点向下

                    QLineF(x + w, y + h, x + w - 10, y + h),  # 右下顶点向左
                    QLineF(x + w, y + h, x + w, y + h - 10)  # 右下顶点向上
                )

    def hoverMoveEvent(self, event):
        super(MoveableItem, self).hoverMoveEvent(event)
        # 鼠标悬停事件
        cursor = self.isInResizeArea(event.pos())
        if self.isResizing or (cursor and self.isSelected()):
            # 正在调整中或者鼠标在可调整区域范围内并且是选中
            self.setCursor(cursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        # 鼠标按下
        super(MoveableItem, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton and self.isInResizeArea(event.pos()):
            self.isResizing = True
            self.prePos = event.pos()

    def mouseReleaseEvent(self, event):
        # 鼠标释放开
        super(MoveableItem, self).mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton and self.isResizing:
            self.isResizing = False
            self.prePos = None

    def mouseMoveEvent(self, event):
        # 鼠标移动
        if self.isResizing and self.prePos:
            rect = self.boundingRect()
            pos = event.pos() - self.prePos
            w = pos.x()
            h = pos.y()
            x = -4 if w > 0 else 4
            y = -4 if h > 0 else 4
            print(x, y, -x, -y, pos)
            self.setRect(rect.adjusted(x, y, -x, -y))
            self.prepareGeometryChange()
        else:
            super(MoveableItem, self).mouseMoveEvent(event)

    def isInResizeArea(self, pos):
        # 检测判断鼠标所在位置是否为四个顶点的范围内
        rect = self.boundingRect()
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

        lx = pos.x() < x + 10
        rx = pos.x() > x + w - 10
        ty = pos.y() < y + 10
        by = pos.y() > y + h - 10
        # 左上角和右下角
        if (lx and ty) or (rx and by):
            return Qt.SizeFDiagCursor
        # 右上角和左下角
        if (rx and ty) or (lx and by):
            return Qt.SizeBDiagCursor
        return 0


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
