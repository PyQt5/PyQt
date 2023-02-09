#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2023/02/09
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: DragGraphics.py
@description:
"""

import json
import os

try:
    from PyQt5.QtCore import QMimeData, Qt
    from PyQt5.QtGui import QDrag, QIcon, QPixmap
    from PyQt5.QtWidgets import (QApplication, QGraphicsPixmapItem,
                                 QGraphicsScene, QGraphicsView, QHBoxLayout,
                                 QListWidget, QListWidgetItem, QTreeWidget,
                                 QTreeWidgetItem, QWidget)
except ImportError:
    from PySide2.QtCore import QMimeData, Qt
    from PySide2.QtGui import QDrag, QIcon, QPixmap
    from PySide2.QtWidgets import (QApplication, QGraphicsPixmapItem,
                                   QGraphicsScene, QGraphicsView, QHBoxLayout,
                                   QListWidget, QListWidgetItem, QTreeWidget,
                                   QTreeWidgetItem, QWidget)


class ListWidget(QListWidget):

    def __init__(self, *args, **kwargs):
        super(ListWidget, self).__init__(*args, **kwargs)
        self.setDragEnabled(True)
        self.setDragDropMode(QListWidget.DragOnly)
        self.setDefaultDropAction(Qt.IgnoreAction)
        self.setEditTriggers(QListWidget.NoEditTriggers)
        self.setResizeMode(QListWidget.Adjust)
        self.setViewMode(QListWidget.IconMode)

    def startDrag(self, supportedActions):
        items = self.selectedItems()
        if not items:
            return
        # 这里就简单的根据名字提示来传递数据了，实际上可以传递任意数据
        data = QMimeData()
        data.setData('application/node-items',
                     json.dumps([item.toolTip() for item in items]).encode())
        # 这里简单显示第一个缩略图
        pixmap = items[0].icon().pixmap(36, 36)
        drag = QDrag(self)
        drag.setMimeData(data)
        drag.setPixmap(pixmap)
        drag.setHotSpot(pixmap.rect().center())
        drag.exec_(supportedActions)


class GraphicsView(QGraphicsView):

    def __init__(self, *args, **kwargs):
        super(GraphicsView, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self._scene = QGraphicsScene(self)  # 场景
        self.setScene(self._scene)

    def dragEnterEvent(self, event):
        """判断拖入的数据是否支持"""
        mimeData = event.mimeData()
        if not mimeData.hasFormat('application/node-items'):
            event.ignore()
            return

        event.acceptProposedAction()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, event):
        """获取拖拽的数据并绘制对于的图形"""
        datas = event.mimeData().data('application/node-items')
        datas = json.loads(datas.data().decode())
        print('datas:', datas)

        path = os.path.join(os.path.dirname(__file__), 'Data/icons')
        for name in datas:
            item = QGraphicsPixmapItem(QPixmap(os.path.join(path, name)))
            item.setFlags(QGraphicsPixmapItem.ItemIsFocusable |
                          QGraphicsPixmapItem.ItemIsMovable)
            self._scene.addItem(item)
            pos = self.mapToScene(event.pos())
            item.moveBy(pos.x(), pos.y())


class DragGraphics(QWidget):

    def __init__(self, *args, **kwargs):
        super(DragGraphics, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QHBoxLayout(self)

        # 左侧树形控制
        self.treeWidget = QTreeWidget(self)
        self.treeWidget.header().setVisible(False)
        self.treeWidget.setMaximumWidth(300)
        layout.addWidget(self.treeWidget)

        # 右侧图形显示
        self.graphicsView = GraphicsView(self)
        layout.addWidget(self.graphicsView)

        self._init_trees()

    def _init_trees(self):
        """初始化树形控件中的图形节点列表"""
        # 1. 获取所有图标
        path = os.path.join(os.path.dirname(__file__), 'Data/icons')
        icons = [os.path.join(path, name) for name in os.listdir(path)]

        # 2. 添加根节点
        for i in range(2):
            item = QTreeWidgetItem(self.treeWidget)
            item.setText(0, 'View %d' % i)

            # 3. 添加子节点作为容器用于存放图标
            itemc = QTreeWidgetItem(item)
            child = ListWidget(self.treeWidget)
            self.treeWidget.setItemWidget(itemc, 0, child)

            # 4. 添加图标
            for icon in icons:
                item = QListWidgetItem(child)
                item.setIcon(QIcon(icon))
                item.setToolTip(os.path.basename(icon))

        self.treeWidget.expandAll()


if __name__ == '__main__':
    import cgitb
    import sys

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    w = DragGraphics()
    w.show()
    sys.exit(app.exec_())
