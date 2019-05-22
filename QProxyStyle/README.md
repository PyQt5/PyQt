# QProxyStyle

- 目录
  - [QTabWidget Tab文字方向](#1qtabwidget-tab文字方向)

## 1、QTabWidget Tab文字方向
[运行 TabTextDirection.py](TabTextDirection.py)

1. 通过 `app.setStyle(TabBarStyle())` 设置代理样式
2. `sizeFromContents` 转置size
3. `drawControl` 绘制文字

![TabTextDirection](ScreenShot/TabTextDirection.png)