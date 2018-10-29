# QGraphicsDropShadowEffect动态边框阴影动画

### 简单说明
 - 1.通过setGraphicsEffect设置控件的边框阴影
 - 2.继承QGraphicsDropShadowEffect实现增加动态属性radius
 - 3.通过QPropertyAnimation属性动画不断改变radius的值并调用setBlurRadius更新半径值

截图

![1](ScreenShot/1.gif)