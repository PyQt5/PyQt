# 简单的右下角气泡提示

### 原理思路：
 - 1.使用QWidget包含一个QLabel，其中QWidget通过paintEvent绘制气泡形状
 - 2.使用QPropertyAnimation属性动画来移动气泡和改变气泡的透明度
 - 3.使用QParallelAnimationGroup动画组来同时运行两个动画

见 [Issues#3](https://github.com/892768447/PyQt/issues/3)

截图

![1](ScreenShot/1.gif)