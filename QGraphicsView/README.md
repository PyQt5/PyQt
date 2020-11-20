# QGraphicsView

- 目录
  - [绘制世界地图](#1绘制世界地图)
  - [添加QWidget](#2添加QWidget)
  - [图片查看器](#3图片查看器)

## 1、绘制世界地图
[运行 WorldMap.py](WorldMap.py)

1. 解析json数据生成 `QPolygonF`
2. 使用Ctrl+滑轮进行放大缩小

![WorldMap](ScreenShot/WorldMap.gif)

## 2、添加QWidget
[运行 AddQWidget.py](AddQWidget.py)

通过 `QGraphicsScene.addWidget` 添加自定义QWidget

![AddQWidget](ScreenShot/AddQWidget.png)

## 3、图片查看器
[运行 ImageView.py](ImageView.py)

支持放大缩小和移动

![ImageView](ScreenShot/ImageView.gif)