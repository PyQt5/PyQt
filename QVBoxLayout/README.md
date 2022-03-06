# QVBoxLayout

- 目录
  - [垂直布局](#1垂直布局)
  - [边距和间隔](#2边距和间隔)

## 1、垂直布局
[查看 BaseVerticalLayout.ui](Data/BaseVerticalLayout.ui)

![BaseVerticalLayout](ScreenShot/BaseVerticalLayout.png)

## 2、边距和间隔
[查看 VerticalLayoutMargin.ui](Data/VerticalLayoutMargin.ui)

1. 通过`setContentsMargins(20, 20, -1, -1)`设置左上右下的边距，-1表示默认值
2. 通过`setSpacing`的`subControlRect`设置控件之间的间隔

![VerticalLayoutMargin](ScreenShot/VerticalLayoutMargin.png)