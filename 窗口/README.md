# 窗口案例

## [1、重启窗口Widget](窗口重启.py)

利用类变量对窗口的变量进行引用，防止被回收（导致窗口一闪而过），重启时先显示新窗口后关闭自己

![截图](ScreenShot/窗口重启.gif)

## [2、分割窗口的分割条重绘](分割窗口的分割条重写.py)

1. 原理在于`QSplitter`在创建分割条的时候会调用`createHandle`函数
1. 通过重新写`createHandle`返回自己的`QSplitterHandle`类
1. 通过`QSplitterHandle`的`paintEvent`实现绘制其它形状，
1. 重写`mousePressEvent`和`mouseMoveEvent`来实现鼠标的其它事件

![截图](ScreenShot/分割窗口的分割条重写.gif)

## [3、简单的窗口贴边隐藏](简单的窗口贴边隐藏.py)

1. 大概思路
    1. 思路是当窗口进入左边，顶部，右边一半时，此时判断窗口的坐标
    1. 如果窗口的x坐标小于0 则需要隐藏到左边
    1. 如果窗口的y坐标小于0 则需要隐藏到顶部
    1. 如果窗口的x坐标大于屏幕宽度-窗口宽度/2 则需要隐藏到右边

2. 事件说明
    1. `mousePressEvent`，鼠标按下事件，主要记录按下的坐标
    1. `mouseMoveEvent`，鼠标移动事件，用于移动窗口
    1. `mouseReleaseEvent`，鼠标弹起事件，用于判断是否需要隐藏窗口
    1. `enterEvent`，鼠标进入事件，用于窗口隐藏后，是否需要暂时显示预览
    1. `leaveEvent`，鼠标离开事件，用于窗口暂时显示后自动隐藏效果
 
## [4、嵌入外部窗口](嵌入外部窗口.py)

1. 使用`SetParent`函数设置外部窗口的`parent`为Qt的窗口
1. Qt使用`QWidget.createWindowContainer(QWindow.fromWinId(窗口ID))`生成QWidget
1. 使用`GetWindowLong`得到原来窗口的样式属性`style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)`和`exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)`
1. 这里还原窗口后不会显示，用spy++发现没有了WS_VISIBLE样式（未解决）

![截图](ScreenShot/嵌入外部窗口.gif)


## [5、简单跟随其它窗口](外部窗口跟随.py)

1. 利用win32gui模块获取目标窗口的句柄
1. 通过句柄获取目标窗口的大小位置，并设置自己的位置
1. 当句柄失效时关闭自己
1. 主要是检测时间，在10毫秒以下很流畅

![截图](ScreenShot/外部窗口跟随.gif)


## [6、简单探测窗口和放大截图](简单探测窗口和放大截图.py)

1. 利用`win32gui`模块获取鼠标所在位置的窗口大小(未去掉边框)和rgb颜色
1. 利用一个全屏的全透明鼠标穿透的窗口（目的在于绘制矩形框和截图）

![截图](ScreenShot/简单探测窗口和放大截图.gif)


## [7、消息对话框倒计时关闭](消息对话框倒计时关闭.py)

1. 通过继承`QMessageBox`实现倒计时关闭的对话框
1. `QTimer`定时器关闭窗口

![截图](ScreenShot/消息对话框倒计时关闭.gif)

## [8、无边框自定义标题栏窗口](无边框自定义标题栏窗口/)

1. 方式一（QWidget）

    1. 使用一个`QWidget`（`FramelessWindow`）作为父窗口, 一个`TitleBar`作为标题栏, 一个`QWidget`作为底部容器
    1. 父窗口`FramelessWindow`设置为背景透明，但是需要绘制一定宽度的透明度很高的矩形边框用来接受鼠标事件（变形鼠标样式进行调整窗口大小）
    1. `TitleBar`的最小化最大化关闭等按钮事件关联到父窗口里
    1. `TitleBar`中的鼠标按下移动事件得到坐标也传递到父窗口调用move方法进行窗口移动

![截图](ScreenShot/无边框自定义标题栏窗口/无边框自定义标题栏窗口.gif)

1. 方式二（windows api）

    1. 使用`win32gui`设置薄边框
    1. 重写`nativeEvent`事件拦截边框的系统边框的显示，并返回各个方向

## 截图
![截图](ScreenShot/无边框自定义标题栏窗口/win无边框调整大小1.jpg)

![截图](ScreenShot/无边框自定义标题栏窗口/win无边框调整大小2.jpg)

![截图](ScreenShot/无边框自定义标题栏窗口/win无边框调整大小3.gif)