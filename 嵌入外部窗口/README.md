# 内嵌外部窗口

### 原理思路：
 - 1.使用SetParent函数设置外部窗口的parent为Qt的窗口
 - 2.Qt使用QWidget.createWindowContainer(QWindow.fromWinId(窗口ID))生成QWidget
 - 3.使用GetWindowLong得到原来窗口的样式属性（style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)和exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)）
 - 4.这里还原窗口后不会显示，用spy++发现没有了WS_VISIBLE样式（未解决）

见 [Issues#3](https://github.com/892768447/PyQt/issues/3)

截图

![1](ScreenShot/1.gif)