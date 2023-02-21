# QListView

- 目录
  - [删除自定义Item](#1删除自定义Item)
  - [自定义可拖拽Item](#2自定义可拖拽Item)
  - [音乐热歌列表](#3音乐热歌列表)
  - [仿折叠控件效果](#4仿折叠控件效果)
  - [列表常用信号](#5列表常用信号)

## 1、删除自定义Item
[运行 DeleteCustomItem.py](DeleteCustomItem.py)

1. 删除item时先要通过`QListWidget.indexFromItem(item).row()`得到它的行数
2. 通过`takeItem`函数取出该Item并删除掉,`item = self.listWidget.takeItem(row)`
3. 移除item对应的自定义控件`self.listWidget.removeItemWidget(item)`
4. 如果是清空所有Item，可以通过循环删除，但是删除的时候行号一直是0即可，原因和删除list数组一样。

![CustomWidgetItem](ScreenShot/DeleteCustomItem.gif)

## 2、自定义可拖拽Item
[运行 DragDrop.py](DragDrop.py)

![CustomWidgetSortItem](ScreenShot/DragDrop.gif)

## 3、音乐热歌列表
[运行 HotPlaylist.py](HotPlaylist.py)

简单思路说明：

 - 利用`QListWidget`设置一些特殊的参数达到可以横向自动显示
 - `QNetworkAccessManager`异步下载网页和图片
 - 滚动到底部触发下一页加载

自定义控件说明：

 - 主要是多个layout和控件的结合，其中图片`QLabel`为自定义，通过`setPixmap`设置图片，重写`paintEvent`绘制底部渐变矩形框和白色文字
 - 字体颜色用qss设置
 - 图标利用了`QSvgWidget`显示，可以是svg 动画（如圆形加载图）

`QListWidget`的参数设置

1. `setFlow(QListWidget.LeftToRight)`
2. `setWrapping(True)`
3. `setResizeMode(QListWidget.Adjust)`

![HotPlaylist](ScreenShot/HotPlaylist.gif)

## 4、仿折叠控件效果
[运行 FoldWidget.py](FoldWidget.py)

1. 利用`QListWidget`设置Item的自定义控件
2. `QListWidget`通过间隔设置`QPushButton`和`CustomWidget`来添加
3. 绑定按钮的选中状态通过`setHidden`设置Item的隐藏和显示
4. 自定义控件中尺寸发生变化后需要调用`adjustSize()`来同步

![FoldWidget](ScreenShot/FoldWidget.gif)

## 5、列表常用信号
[运行 SignalsExample.py](SignalsExample.py)

根据官网文档 https://doc.qt.io/qt-5/qlistwidget.html#signals 中的信号介绍编写

![SignalsExample](ScreenShot/SignalsExample.gif)