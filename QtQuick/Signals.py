#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月18日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QtQuick.Signals
@description: 信号槽
"""

import sys
from time import time

try:
    from PyQt5.QtCore import QCoreApplication, Qt, pyqtSlot, pyqtSignal, QTimer
    from PyQt5.QtQml import QQmlApplicationEngine
    from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, \
        QPushButton, QTextBrowser
except ImportError:
    from PySide2.QtCore import QCoreApplication, Qt, Slot as pyqtSlot, Signal as pyqtSignal, QTimer
    from PySide2.QtQml import QQmlApplicationEngine
    from PySide2.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, \
        QPushButton, QTextBrowser

QML = """import QtQuick 2.0
import QtQuick.Controls 1.6
import QtQuick.Layouts 1.3

ApplicationWindow {
    visible: true
    width: 400
    height: 400
    id: root
    title: "editor"

    // 定义信号槽
    signal valueChanged(int value)
    
    Component.onCompleted: {
        // 绑定信号槽到python中的函数
        valueChanged.connect(_Window.onValueChanged)
        // 绑定python中的信号到qml中的函数
        _Window.timerSignal.connect(appendText)
    }
    
    function appendText(text) {
        // 定义添加文字函数
        textArea.append(text)
    }

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent

        Button {
            id: button
            text: qsTr("Button")
            Layout.fillWidth: true
            onClicked: {
                // 点击按钮调用python中的函数并得到返回值
                var ret = _Window.testSlot("Button")
                textArea.append("我调用了testSlot函数得到返回值: " + ret)
            }
        }

        Slider {
            id: sliderHorizontal
            Layout.fillWidth: true
            stepSize: 1
            minimumValue: 0
            maximumValue: 100
            // 拉动条值改变时发送信号
            onValueChanged: root.valueChanged(value)
        }

        TextArea {
            id: textArea
            Layout.fillWidth: true
        }
    }

}
"""


class Window(QWidget):
    # 定义一个时间信号
    timerSignal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton('Python调用qml中的函数',
                                     self, clicked=self.callQmlFunc))
        self.resultView = QTextBrowser(self)
        layout.addWidget(self.resultView)
        self._timer = QTimer(self, timeout=self.onTimeout)
        self._timer.start(2000)

    def onTimeout(self):
        # 定时器发送信号通知qml
        self.timerSignal.emit('定时器发来:' + str(time()))

    def callQmlFunc(self):
        # 主动调用qml中的appendText函数
        engine.rootObjects()[0].appendText('我是被Python调用了')

    @pyqtSlot(int)
    def onValueChanged(self, value):
        # qml中的自定义信号valueChanged所绑定的槽函数
        self.resultView.append('拉动条值: %s' % value)

    @pyqtSlot(str, result=str)  # 可以获取返回值
    def testSlot(self, name):
        # 被qml调用的函数
        self.resultView.append('我被主动调用: %s' % name)
        return str(len(name))


if __name__ == '__main__':
    try:
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    except:
        pass

    app = QApplication(sys.argv)

    # 测试界面
    w = Window()
    w.resize(400, 400)
    w.show()
    w.move(400, 400)

    engine = QQmlApplicationEngine()
    # 提供一个沟通的对象_Window，必须是要继承QObject的类
    engine.rootContext().setContextProperty('_Window', w)

    engine.objectCreated.connect(
        lambda obj, _: QMessageBox.critical(None, '错误', '运行失败，请检查') if not obj else 0)
    engine.loadData(QML.encode())

    sys.exit(app.exec_())
