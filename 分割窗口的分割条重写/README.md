# 分割窗口的分割条重绘

原理在于QSplitter在创建分割条的时候会调用createHandle函数

于是通过重新写createHandle返回自己的QSplitterHandle类

并通过QSplitterHandle的paintEvent实现绘制其它形状，
重写mousePressEvent和mouseMoveEvent来实现鼠标的其它事件

## 截图
![截图](ScreenShot/1.gif)