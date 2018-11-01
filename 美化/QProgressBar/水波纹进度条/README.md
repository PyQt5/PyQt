# 矩形/圆形 水波纹进度条

 
### 简单说明
 - 利用正弦函数根据0-width的范围计算y坐标
 - 利用QPainterPath矩形或者圆形作为背景
 - 用QPainterPath把y坐标用lineTo连接起来形成一个U字形+上方波浪的闭合区间

截图

![1](ScreenShot/1.gif)