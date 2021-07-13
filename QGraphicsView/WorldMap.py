#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年12月17日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: WorldMap
@description: 
"""
import json
import math

try:
    from PyQt5.QtCore import Qt, QPointF, QRectF
    from PyQt5.QtGui import QColor, QPainter, QPolygonF, QPen, QBrush
    from PyQt5.QtOpenGL import QGLFormat
    from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPolygonItem
except ImportError:
    from PySide2.QtCore import Qt, QPointF, QRectF
    from PySide2.QtGui import QColor, QPainter, QPolygonF, QPen, QBrush
    from PySide2.QtOpenGL import QGLFormat
    from PySide2.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPolygonItem


class GraphicsView(QGraphicsView):
    # 背景区域颜色
    backgroundColor = QColor(31, 31, 47)
    # 边框颜色
    borderColor = QColor(58, 58, 90)

    def __init__(self, *args, **kwargs):
        super(GraphicsView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        # 设置背景颜色
        self.setBackgroundBrush(self.backgroundColor)
        '''
        #参考 http://doc.qt.io/qt-5/qgraphicsview.html#CacheModeFlag-enum
        CacheNone                    不使用缓存
        CacheBackground              缓存背景
        '''
        self.setCacheMode(self.CacheBackground)
        '''
        #参考 http://doc.qt.io/qt-5/qgraphicsview.html#DragMode-enum
        NoDrag                       什么都没发生; 鼠标事件被忽略。
        ScrollHandDrag               光标变成指针，拖动鼠标将滚动滚动条。 该模式可以在交互式和非交互式模式下工作。
        RubberBandDrag               拖动鼠标将设置橡皮筋几何形状，并选择橡皮筋所覆盖的所有项目。 对于非交互式视图，此模式被禁用。
        '''
        self.setDragMode(self.ScrollHandDrag)
        '''
        #参考 http://doc.qt.io/qt-5/qgraphicsview.html#OptimizationFlag-enum
        DontClipPainter              已过时
        DontSavePainterState         渲染时，QGraphicsView在渲染背景或前景时以及渲染每个项目时保护painter状态（请参阅QPainter.save()）。 这允许你离开painter处于改变状态（即你可以调用QPainter.setPen()或QPainter.setBrush()，而不需要在绘制之后恢复状态）。 但是，如果项目一致地恢复状态，则应启用此标志以防止QGraphicsView执行相同的操作。
        DontAdjustForAntialiasing    禁用QGraphicsView的抗锯齿自动调整曝光区域。 在QGraphicsItem.boundingRect()的边界上渲染反锯齿线的项目可能会导致渲染部分线外。 为了防止渲染失真，QGraphicsView在所有方向上将所有曝光区域扩展2个像素。 如果启用此标志，QGraphicsView将不再执行这些调整，最大限度地减少需要重绘的区域，从而提高性能。 一个常见的副作用是，使用抗锯齿功能进行绘制的项目可能会在移动时在画面上留下绘画痕迹。
        IndirectPainting             从Qt 4.6开始，恢复调用QGraphicsView.drawItems()和QGraphicsScene.drawItems()的旧绘画算法。 仅用于与旧代码的兼容性。
        '''
        self.setOptimizationFlag(self.DontSavePainterState)
        '''
        #参考 http://doc.qt.io/qt-5/qpainter.html#RenderHint-enum
        Antialiasing                 抗锯齿
        TextAntialiasing             文本抗锯齿
        SmoothPixmapTransform        平滑像素变换算法
        HighQualityAntialiasing      请改用Antialiasing
        NonCosmeticDefaultPen        已过时
        Qt4CompatiblePainting        从Qt4移植到Qt5可能有用
        '''
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform)
        if QGLFormat.hasOpenGL():
            self.setRenderHint(QPainter.HighQualityAntialiasing)
        '''
        #当视图被调整大小时，视图如何定位场景。使用这个属性来决定当视口控件的大小改变时，如何在视口中定位场景。 缺省行为NoAnchor在调整大小的过程中不改变场景的位置; 视图的左上角将显示为在调整大小时被锚定。请注意，只有场景的一部分可见（即有滚动条时），此属性的效果才明显。 否则，如果整个场景适合视图，QGraphicsScene使用视图对齐将视景中的场景定位。 
        #参考 http://doc.qt.io/qt-5/qgraphicsview.html#ViewportAnchor-enum
        NoAnchor                     视图保持场景的位置不变
        AnchorViewCenter             视图中心被用作锚点。
        AnchorUnderMouse             鼠标当前位置被用作锚点
        '''
        self.setResizeAnchor(self.AnchorUnderMouse)
        '''
        Rubber选择模式
        #参考 http://doc.qt.io/qt-5/qt.html#ItemSelectionMode-enum
        ContainsItemShape            输出列表仅包含形状完全包含在选择区域内的项目。 不包括与区域轮廓相交的项目。
        IntersectsItemShape          默认，输出列表包含其形状完全包含在选择区域内的项目以及与区域轮廓相交的项目。
        ContainsItemBoundingRect     输出列表仅包含边界矩形完全包含在选择区域内的项目。 不包括与区域轮廓相交的项目。
        IntersectsItemBoundingRect   输出列表包含边界矩形完全包含在选择区域内的项目以及与区域轮廓相交的项目。 这种方法通常用于确定需要重绘的区域。
        '''
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
        '''
        #在转换过程中如何定位视图。QGraphicsView使用这个属性决定当变换矩阵改变时如何在视口中定位场景，并且视图的坐标系被变换。 默认行为AnchorViewCenter确保在视图中心的场景点在变换过程中保持不变（例如，在旋转时，场景将围绕视图的中心旋转）。请注意，只有场景的一部分可见（即有滚动条时），此属性的效果才明显。 否则，如果整个场景适合视图，QGraphicsScene使用视图对齐将视景中的场景定位。
        #参考 http://doc.qt.io/qt-5/qgraphicsview.html#ViewportAnchor-enum
        NoAnchor                     视图保持场景的位置不变
        AnchorViewCenter             视图中心被用作锚点。
        AnchorUnderMouse             鼠标当前位置被用作锚点
        '''
        self.setTransformationAnchor(self.AnchorUnderMouse)
        #         if QGLFormat.hasOpenGL():  # 如果开启了OpenGL则使用OpenGL Widget
        #             self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))
        '''
        #参考 http://doc.qt.io/qt-5/qgraphicsview.html#ViewportUpdateMode-enum
        FullViewportUpdate           当场景的任何可见部分改变或重新显示时，QGraphicsView将更新整个视口。 当QGraphicsView花费更多的时间来计算绘制的内容（比如重复更新很多小项目）时，这种方法是最快的。 这是不支持部分更新（如QGLWidget）的视口以及需要禁用滚动优化的视口的首选更新模式。
        MinimalViewportUpdate        QGraphicsView将确定需要重绘的最小视口区域，通过避免重绘未改变的区域来最小化绘图时间。 这是QGraphicsView的默认模式。 虽然这种方法提供了一般的最佳性能，但如果场景中有很多小的可见变化，QGraphicsView最终可能花费更多的时间来寻找最小化的方法。
        SmartViewportUpdate          QGraphicsView将尝试通过分析需要重绘的区域来找到最佳的更新模式。
        BoundingRectViewportUpdate   视口中所有更改的边界矩形将被重绘。 这种模式的优点是，QGraphicsView只搜索一个区域的变化，最大限度地减少了花在确定需要重绘的时间。 缺点是还没有改变的地方也需要重新绘制。
        NoViewportUpdate             当场景改变时，QGraphicsView将永远不会更新它的视口。 预计用户将控制所有更新。 此模式禁用QGraphicsView中的所有（可能较慢）项目可见性测试，适用于要求固定帧速率或视口以其他方式在外部进行更新的场景。
        '''
        self.setViewportUpdateMode(self.SmartViewportUpdate)
        # 设置场景(根据地图的经纬度,并让原点显示在屏幕中间)
        self._scene = QGraphicsScene(-180, -90, 360, 180, self)
        self.setScene(self._scene)

        # 初始化地图
        self.initMap()

    def wheelEvent(self, event):
        # 滑轮事件
        if event.modifiers() & Qt.ControlModifier:
            self.scaleView(math.pow(2.0, -event.angleDelta().y() / 240.0))
            return event.accept()
        super(GraphicsView, self).wheelEvent(event)

    def scaleView(self, scaleFactor):
        factor = self.transform().scale(
            scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)

    def initMap(self):
        features = json.load(
            open("Data/world.json", encoding="utf8")).get("features")
        for feature in features:
            geometry = feature.get("geometry")
            if not geometry:
                continue
            _type = geometry.get("type")
            coordinates = geometry.get("coordinates")
            for coordinate in coordinates:
                if _type == "Polygon":
                    polygon = QPolygonF(
                        [QPointF(latitude, -longitude) for latitude, longitude in coordinate])
                    item = QGraphicsPolygonItem(polygon)
                    item.setPen(QPen(self.borderColor, 0))
                    item.setBrush(QBrush(self.backgroundColor))
                    item.setPos(0, 0)
                    self._scene.addItem(item)
                elif _type == "MultiPolygon":
                    for _coordinate in coordinate:
                        polygon = QPolygonF(
                            [QPointF(latitude, -longitude) for latitude, longitude in _coordinate])
                        item = QGraphicsPolygonItem(polygon)
                        item.setPen(QPen(self.borderColor, 0))
                        item.setBrush(QBrush(self.backgroundColor))
                        item.setPos(0, 0)
                        self._scene.addItem(item)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    print("OpenGL Status:", QGLFormat.hasOpenGL())
    view = GraphicsView()
    view.setWindowTitle("世界地图")
    view.show()
    sys.exit(app.exec_())
