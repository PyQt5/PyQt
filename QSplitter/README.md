# QSplitter

- 目录
  - [分割窗口的分割条重绘](#1分割窗口的分割条重绘)

## 1、分割窗口的分割条重绘
[运行 RewriteHandle.py](RewriteHandle.py)

1. 原理在于`QSplitter`在创建分割条的时候会调用`createHandle`函数
1. 通过重新写`createHandle`返回自己的`QSplitterHandle`类
1. 通过`QSplitterHandle`的`paintEvent`实现绘制其它形状，
1. 重写`mousePressEvent`和`mouseMoveEvent`来实现鼠标的其它事件

![RewriteHandle](ScreenShot/RewriteHandle.gif)