# 界面美化

## QPushButton

### 1. [按钮常见样式](QPushButton/按钮常见样式.py)

主要改变背景颜色、鼠标按下颜色、鼠标悬停颜色、圆角、圆形、文字颜色

![截图](QPushButton/ScreenShot/按钮常见样式.gif)

### 2. [按钮进度动画](QPushButton/按钮进度动画)

1. [按钮字体旋转动画](QPushButton/按钮进度动画/按钮字体旋转动画.py)

    利用字体，使用FontAwesome字体来显示一个圆形进度条，然后利用旋转动画

    ![截图](QPushButton/按钮进度动画/ScreenShot/按钮字体旋转动画.gif)

2. [按钮底部线条动画](QPushButton/按钮进度动画/按钮底部线条动画.py)

    在按钮下方画一条线，根据百分值绘制

    ![截图](QPushButton/按钮进度动画/ScreenShot/按钮底部线条动画.gif)

## QLabel

1. [圆形图片](QLabel/圆形图片.py)

    使用`QPainter`的`setClipPath`方法结合`QPainterPath`对图片进行裁剪从而实现圆形图片。

    ![截图](QLabel/ScreenShot/圆形图片.png)