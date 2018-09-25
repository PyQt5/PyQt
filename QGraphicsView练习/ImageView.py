#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月23日
@author: Irony
@site: https://pyqt5.com, https://github.com/892768447
@email: 892768447@qq.com
@file: ImageView
@description: 图片查看
"""
from PyQt5.QtCore import QStandardPaths, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtOpenGL import QGLFormat
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QFileDialog, \
    QGraphicsItem


__Author__ = 'By: Irony\nQQ: 892768447\nEmail: 892768447@qq.com'
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class GraphicsView(QGraphicsView):

    # 背景区域颜色
    backgroundColor = QColor(28, 31, 34)

    def __init__(self, *args, **kwargs):
        super(GraphicsView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        # 设置背景颜色
        self.setBackgroundBrush(self.backgroundColor)
        # 缓存背景
        self.setCacheMode(self.CacheBackground)
        # 设置拖拽样式
        # self.setDragMode(self.ScrollHandDrag)
        self.setRenderHints(
            QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        # opengl
        if QGLFormat.hasOpenGL():
            self.setRenderHint(QPainter.HighQualityAntialiasing)
        # 尝试通过分析需要重绘的区域来找到最佳的更新模式
        self.setViewportUpdateMode(self.SmartViewportUpdate)
        self._scene = QGraphicsScene(-400, -300, 800, 600, self)
        self.setScene(self._scene)

        # 图片item
        self._itemImage = None

    def keyReleaseEvent(self, event):
        """按键处理事件"""
        self._scaleImage(event)
        super(GraphicsView, self).keyReleaseEvent(event)

    def closeEvent(self, event):
        """窗口关闭时清空场景中的所有item"""
        self._scene.clear()
        self._itemImage = None
        super(GraphicsView, self).closeEvent(event)

    def _scaleImage(self, event):
        """缩放图片操作"""
        if not self._itemImage:
            return
        scale = self._itemImage.scale()
        if event.key() == Qt.Key_Plus:
            # 放大
            if scale >= 0.91:
                return
            self._itemImage.setScale(scale + 0.1)
        elif event.key() == Qt.Key_Minus:
            # 缩小
            if scale <= 0.11:
                return
            self._itemImage.setScale(scale - 0.1)

    def loadImage(self):
        path, _ = QFileDialog.getOpenFileName(
            self, '请选择图片', QStandardPaths.writableLocation(QStandardPaths.DesktopLocation), '图片文件(*.jpg *.png)')
        if not path:
            return
        if self._itemImage:
            # 删除以前的item
            self._scene.removeItem(self._itemImage)
            del self._itemImage
        self._itemImage = self._scene.addPixmap(QPixmap(path))
        self._itemImage.setFlag(QGraphicsItem.ItemIsMovable)
        self._itemImage.setScale(0.1)  # 默认加载比例

        size = self._itemImage.pixmap().size()
        # 调整图片在中间
        self._itemImage.setPos(
            -size.width() * self._itemImage.scale() / 2,
            -size.height() * self._itemImage.scale() / 2
        )

if __name__ == '__main__':
    import sys
    import os
    print(os.getpid())
    from PyQt5.QtWidgets import QApplication, QPushButton
    app = QApplication(sys.argv)
    w = GraphicsView()
    w.show()
    ww = QPushButton('选择文件', clicked=w.loadImage)
    ww.show()
    sys.exit(app.exec_())
