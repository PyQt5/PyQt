# QVBoxLayout

- 目录
  - [垂直布局](#1垂直布局)
  - [边距和间隔](#2边距和间隔)
  - [比例分配](#3比例分配)

## 1、垂直布局
[查看 BaseVerticalLayout.ui](Data/BaseVerticalLayout.ui)

![BaseVerticalLayout](ScreenShot/BaseVerticalLayout.png)

## 2、边距和间隔
[查看 VerticalLayoutMargin.ui](Data/VerticalLayoutMargin.ui)

1. 通过`setContentsMargins(20, 20, -1, -1)`设置左上右下的边距，-1表示默认值
2. 通过`setSpacing`设置控件之间的间隔

![VerticalLayoutMargin](ScreenShot/VerticalLayoutMargin.png)

## 3、比例分配
[查看 VerticalLayoutStretch.ui](Data/VerticalLayoutStretch.ui)

通过`setStretch`设置各个部分的占比 分别为：1/6 2/6 3/6

```python
self.verticalLayout.setStretch(0, 1)
self.verticalLayout.setStretch(1, 2)
self.verticalLayout.setStretch(2, 3)
```

![VerticalLayoutStretch](ScreenShot/VerticalLayoutStretch.png)