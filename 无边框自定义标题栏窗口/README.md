# 无边框自定义标题栏窗口

### [Python3.4.4 or Python3.5][PyQt5]

原理说明:

 - 使用一个QWidget（FramelessWindow）作为父窗口, 一个TitleBar作为标题栏, 一个QWidget作为底部容器
 - 父窗口FramelessWindow设置为背景透明，但是需要绘制一定宽度的透明度很高的矩形边框用来接受鼠标事件（变形鼠标样式进行调整窗口大小）
 - TitleBar的最小化最大化关闭等按钮事件关联到父窗口里
 - TitleBar中的鼠标按下移动事件得到坐标也传递到父窗口调用move方法进行窗口移动

使用方法：

```
class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QPushButton('按钮', self))
        layout.addWidget(QTextEdit(self))


# 样式
StyleSheet = """
/*标题栏*/
TitleBar {
    background-color: rgb(54, 157, 180);
}

/*最小化最大化关闭按钮通用默认背景*/
#buttonMinimum,#buttonMaximum,#buttonClose {
    border: none;
    background-color: rgb(54, 157, 180);
}

/*悬停*/
#buttonMinimum:hover,#buttonMaximum:hover {
    background-color: rgb(48, 141, 162);
}
#buttonClose:hover {
    color: white;
    background-color: rgb(232, 17, 35);
}

/*鼠标按下不放*/
#buttonMinimum:pressed,#buttonMaximum:pressed {
    background-color: rgb(44, 125, 144);
}
#buttonClose:pressed {
    color: white;
    background-color: rgb(161, 73, 92);
}
"""

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    w = FramelessWindow()
    w.setWindowTitle('测试标题栏')
    w.setWindowIcon(QIcon('Qt.ico'))
    w.setWidget(MainWindow(w))  # 把自己的窗口添加进来
    w.show()
    sys.exit(app.exec_())

```

## 截图
![截图](ScreenShot/1.gif)



# 利用windows api

原理说明:

 - 使用win32gui设置薄边框
 - 重写nativeEvent事件拦截边框的系统边框的显示，并返回各个方向

## 截图
![截图](ScreenShot/1.jpg)

![截图](ScreenShot/1.jpg)

![截图](ScreenShot/3.gif)