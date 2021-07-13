#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021/4/15
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ImageView
@description: 
"""
import os

try:
    from PyQt5.QtCore import QPointF, Qt, QRectF, QSizeF
    from PyQt5.QtGui import QStandardItem, QStandardItemModel, QPainter, QColor, QImage, QPixmap
    from PyQt5.QtWidgets import QApplication, QListView, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene
except ImportError:
    from PySide2.QtCore import QPointF, Qt, QRectF, QSizeF
    from PySide2.QtGui import QStandardItem, QStandardItemModel, QPainter, QColor, QImage, QPixmap
    from PySide2.QtWidgets import QApplication, QListView, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene

ScrollPixel = 40


class BigImageView(QGraphicsView):
    """图片查看控件"""

    def __init__(self, *args, **kwargs):
        image = kwargs.pop('image', None)
        background = kwargs.pop('background', None)
        super(BigImageView, self).__init__(*args, **kwargs)
        self.setCursor(Qt.OpenHandCursor)
        self.setBackground(background)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                            QPainter.SmoothPixmapTransform)
        self.setCacheMode(self.CacheBackground)
        self.setViewportUpdateMode(self.SmartViewportUpdate)
        self._item = QGraphicsPixmapItem()  # 放置图像
        self._item.setFlags(QGraphicsPixmapItem.ItemIsFocusable |
                            QGraphicsPixmapItem.ItemIsMovable)
        self._scene = QGraphicsScene(self)  # 场景
        self.setScene(self._scene)
        self._scene.addItem(self._item)
        rect = QApplication.instance().desktop().availableGeometry()
        self.resize(int(rect.width() * 2 / 3), int(rect.height() * 2 / 3))

        self.pixmap = None
        self._delta = 0.1  # 缩放
        self.setPixmap(image)

    def setBackground(self, color):
        """设置背景颜色
        :param color: 背景颜色
        :type color: QColor or str or GlobalColor
        """
        if isinstance(color, QColor):
            self.setBackgroundBrush(color)
        elif isinstance(color, (str, Qt.GlobalColor)):
            color = QColor(color)
            if color.isValid():
                self.setBackgroundBrush(color)

    def setPixmap(self, pixmap, fitIn=True):
        """加载图片
        :param pixmap: 图片或者图片路径
        :param fitIn: 是否适应
        :type pixmap: QPixmap or QImage or str
        :type fitIn: bool
        """
        if isinstance(pixmap, QPixmap):
            self.pixmap = pixmap
        elif isinstance(pixmap, QImage):
            self.pixmap = QPixmap.fromImage(pixmap)
        elif isinstance(pixmap, str) and os.path.isfile(pixmap):
            self.pixmap = QPixmap(pixmap)
        else:
            return
        self._item.setPixmap(self.pixmap)
        self._item.update()
        self.setSceneDims()
        if fitIn:
            self.fitInView(QRectF(self._item.pos(), QSizeF(
                self.pixmap.size())), Qt.KeepAspectRatio)
        self.update()

    def setSceneDims(self):
        if not self.pixmap:
            return
        self.setSceneRect(QRectF(QPointF(0, 0), QPointF(self.pixmap.width(), self.pixmap.height())))

    def fitInView(self, rect, flags=Qt.IgnoreAspectRatio):
        """剧中适应
        :param rect: 矩形范围
        :param flags:
        :return:
        """
        if not self.scene() or rect.isNull():
            return
        unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
        self.scale(1 / unity.width(), 1 / unity.height())
        viewRect = self.viewport().rect()
        sceneRect = self.transform().mapRect(rect)
        x_ratio = viewRect.width() / sceneRect.width()
        y_ratio = viewRect.height() / sceneRect.height()
        if flags == Qt.KeepAspectRatio:
            x_ratio = y_ratio = min(x_ratio, y_ratio)
        elif flags == Qt.KeepAspectRatioByExpanding:
            x_ratio = y_ratio = max(x_ratio, y_ratio)
        self.scale(x_ratio, y_ratio)
        self.centerOn(rect.center())

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def zoomIn(self):
        """放大"""
        self.zoom(1 + self._delta)

    def zoomOut(self):
        """缩小"""
        self.zoom(1 - self._delta)

    def zoom(self, factor):
        """缩放
        :param factor: 缩放的比例因子
        """
        _factor = self.transform().scale(
            factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()
        if _factor < 0.07 or _factor > 100:
            # 防止过大过小
            return
        self.scale(factor, factor)


class ImageView(QListView):

    def __init__(self, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self.setFrameShape(self.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(self.NoEditTriggers)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(self.DragDrop)
        self.setDefaultDropAction(Qt.IgnoreAction)
        self.setSelectionMode(self.ExtendedSelection)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSpacing(6)
        self.setViewMode(self.IconMode)
        self.setWordWrap(True)
        self.setSelectionRectVisible(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 解决拖动到顶部或者底部自动滚动
        self.setAutoScrollMargin(150)
        self.verticalScrollBar().setSingleStep(ScrollPixel)
        # 设置model
        self.dmodel = QStandardItemModel(self)
        self.setModel(self.dmodel)

        # 大图控件
        self.bigView = BigImageView(background='#323232')

    def addItem(self, image):
        if isinstance(image, str):
            image = QPixmap(image)
        # 添加一个item
        item = QStandardItem()
        # 记录原始图片
        item.setData(image, Qt.UserRole + 1)  # 用于双击的时候取出来
        # 缩放成小图并显示
        item.setData(image.scaled(60, 60, Qt.IgnoreAspectRatio, Qt.SmoothTransformation), Qt.DecorationRole)
        # 添加item到界面中
        self.dmodel.appendRow(item)

    def count(self):
        return self.dmodel.rowCount()

    def setCurrentRow(self, row):
        self.setCurrentIndex(self.dmodel.index(row, 0))

    def currentRow(self):
        return self.currentIndex().row()

    def updateGeometries(self):
        # 一次滑动20px
        super(ImageView, self).updateGeometries()
        self.verticalScrollBar().setSingleStep(ScrollPixel)

    def closeEvent(self, event):
        # 关闭预览窗口
        self.bigView.close()
        super(ImageView, self).closeEvent(event)

    def wheelEvent(self, event):
        # 修复滑动bug
        if self.flow() == QListView.LeftToRight:
            bar = self.horizontalScrollBar()
            value = ScrollPixel if event.angleDelta().y() < 0 else (0 - ScrollPixel)
            bar.setSliderPosition(bar.value() + value)
        else:
            super(ImageView, self).wheelEvent(event)

    def mouseDoubleClickEvent(self, event):
        # 列表双击,如果有item则进入item处理流程,否则调用打开图片功能
        index = self.indexAt(event.pos())
        if index and index.isValid():
            item = self.dmodel.itemFromIndex(index)
            if item:
                # 取出原图用来新窗口显示
                image = item.data(Qt.UserRole + 1)
                self.bigView.setPixmap(image)
                self.bigView.show()
            return
        super(ImageView, self).mouseDoubleClickEvent(event)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    w = ImageView()
    w.show()

    # 添加模拟图片
    for i in range(3):
        for name in os.listdir('ScreenShot'):
            w.addItem(os.path.join('ScreenShot', name))
    sys.exit(app.exec_())
