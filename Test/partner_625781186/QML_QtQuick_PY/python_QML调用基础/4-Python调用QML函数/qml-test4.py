# -*- coding: utf-8 -*-
'''
（4）Python调用QML函数

QML中创建一个函数，

Python中创建一个rootObject对象，并连接这个函数，

例子中，每隔1s，指针会旋转45 deg;。
'''
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

if __name__ == '__main__':
    path = 'test4.qml'   # 加载的QML文件

    app = QGuiApplication([])
    view = QQuickView()
    view.engine().quit.connect(app.quit)
    view.setSource(QUrl(path))
    view.show()

    timer = QTimer()
    timer.start(2000)
    root = view.rootObject()
    timer.timeout.connect(root.updateRotater)  # 调用QML函数

    app.exec_()
