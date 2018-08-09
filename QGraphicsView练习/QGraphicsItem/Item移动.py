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
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsView, QGraphicsScene


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class MoveableItem(QGraphicsRectItem):

    def __init__(self, *args, **kwargs):
        super(MoveableItem, self).__init__(*args, **kwargs)
        self.setFlag(self.ItemIsMovable)  # 设置为可以动
        self.setBrush(QColor(247, 160, 57))  # 设置背景颜色


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
        self._scene = QGraphicsScene()
        self.setScene(self._scene)
        self.setSceneRect(0, 0, self.width(), self.height())

        self._scene.addItem(MoveableItem(100, 100, 200, 200))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = ImageWidget()
    w.show()
    sys.exit(app.exec_())
