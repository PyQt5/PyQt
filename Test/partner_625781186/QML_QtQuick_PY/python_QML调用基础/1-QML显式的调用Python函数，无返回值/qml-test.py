#!/usr/bin/env python
'''
（1）QML显式的调用Python函数

定义一个类，并继承QtCore.QObject对象，并使用@修饰符修饰pyqtSlot

创建rootContext对象，并使用setContextProperty（string, object）注册对象，    
这样在QML中就可以调用这个函数了。

这个例子运行后，如果点击鼠标的话，会在控制台打印字符串。
'''
from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView


class MyClass(QObject):
    @pyqtSlot(str)    # 输入参数为str类型
    def outputString(self, string):
        print(string)


if __name__ == '__main__':
    
    app = QGuiApplication([])
    
    path = 'test.qml'   # 加载的QML文件
    con = MyClass()

    view = QQuickView()
    view.engine().quit.connect(app.quit)
    view.setSource(QUrl(path))

    context = view.rootContext()
    context.setContextProperty("con", con)

    view.show()
    app.exec_()
