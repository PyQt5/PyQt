# 动画特效

使用QPropertyAnimation属性类动画（支持的属性有限）

## [1、窗口淡入淡出](窗口淡入淡出.py)

1. 使用`QPropertyAnimation`对窗口的`windowOpacity`透明度属性进行修改
1. 窗口启动时开启透明度0-->1的动画
    1. 尝试先取消动画完成后关闭窗口的信号（使用同一个动画对象，在关闭窗口动画的时候连接了动画结束后关闭窗口的信号）
    1. 停止旧动画开启新动画
1. 窗口关闭时开启透明度1-->0的动画
    1. 停止就动画
    1. 绑定动画完成后`finished`信号连接到`close`关闭窗口函数

![截图](ScreenShot/窗口淡入淡出.gif)
   
## [2、右键菜单动画](右键菜单动画.py)

1. 使用`QPropertyAnimation`对菜单控件的`geometry`属性进行修改
1. 当菜单事件`contextMenuEvent`触发时调用动画启动，同时显示菜单

![截图](ScreenShot/右键菜单动画.gif)
   
## [3、按钮放大缩小动画](按钮放大缩小动画.py)

1. 使用`QPropertyAnimation`对按钮的`geometry`属性进行修改
1. 针对按钮在布局中或者没有在布局中两种情况，需要对主窗口的`showEvent`和`resizeEvent`两个事件进行重写，从而达到更新按钮的最新`geometry`值
1. 主动调用按钮的`updatePos`函数来更新`geometry`值

比如：

```python
def showEvent(self, event):
    super(TestWindow, self).showEvent(event)
    # 更新按钮的位置
    self.button1.updatePos()
    # 针对不在控件中的按钮
    self.button2.move(self.width() - self.button2.width() - 15,
                      self.height() - self.button2.height() - 10)
    self.button2.updatePos()

def resizeEvent(self, event):
    super(TestWindow, self).resizeEvent(event)
    # 更新按钮的位置
    self.button1.updatePos()
    # 针对不在控件中的按钮
    self.button2.move(self.width() - self.button2.width() - 15,
                      self.height() - self.button2.height() - 10)
    self.button2.updatePos()
```

![截图](ScreenShot/按钮放大缩小动画.gif)