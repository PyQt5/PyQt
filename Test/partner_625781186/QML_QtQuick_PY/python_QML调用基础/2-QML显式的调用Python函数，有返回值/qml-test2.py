#!/usr/bin/env python
'''
（2）QML显式的调用Python函数，并有返回

这个例子跟上一个相类似，只是这次调用Python的函数具有返回值功能。

运行程序后，点击鼠标，左上角会显示数字30。
'''
from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView


class MyClass(QObject):
    @pyqtSlot(int, result=str)    # 声明为槽，输入参数为int类型，返回值为str类型
    def returnValue(self, value):
        return str(value+10)

if __name__ == '__main__':
    path = 'test2.qml'   # 加载的QML文件
    app = QGuiApplication([])

    con = MyClass()

    view = QQuickView()
    view.engine().quit.connect(app.quit)
    view.setSource(QUrl(path))
    
    context = view.rootContext()
    context.setContextProperty("con", con)

    view.show()
    app.exec_()
