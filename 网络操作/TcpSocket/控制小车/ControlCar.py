#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWidgets import QWidget


# Created on 2018年4月18日
# author: Irony
# site: https://github.com/892768447
# email: 892768447@qq.com
# file: ControlCar
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class ControlCar(QWidget):

    HOST = "127.0.0.1"
    PORT = 8888

    def __init__(self, *args, **kwargs):
        super(ControlCar, self).__init__(*args, **kwargs)
        self._conn = None
        # 加载UI文件
        uic.loadUi('carui.ui', self)
        self.resize(800, 600)
        # 绑定连接按钮信号
        self.buttonConnect.clicked.connect(self.doConnect)
        # 绑定拉动信号
        self.sliderForward.valueChanged.connect(self.doForward)
        self.sliderBackward.valueChanged.connect(self.doBackward)
        self.sliderLeft.valueChanged.connect(self.doLeft)
        self.sliderRight.valueChanged.connect(self.doRight)
        # 设置初始拉动条不能用
        self.sliderForward.setEnabled(False)
        self.sliderBackward.setEnabled(False)
        self.sliderLeft.setEnabled(False)
        self.sliderRight.setEnabled(False)

    def closeEvent(self, event):
        """窗口关闭事件"""
        if self._conn:
            self._conn.close()
            self._conn.deleteLater()
            del self._conn
            self._conn = None
        super(ControlCar, self).closeEvent(event)

    def doConnect(self):
        """连接服务器"""
        self.buttonConnect.setEnabled(False)
        if self._conn:
            self._conn.close()
            self._conn.deleteLater()
            del self._conn
            self._conn = None
        self.browserResult.append('正在连接服务器')
        self._conn = QTcpSocket(self)
        self._conn.connected.connect(self.onConnected)  # 绑定连接成功信号
        self._conn.disconnected.connect(self.onDisconnected)  # 绑定连接丢失信号
        self._conn.readyRead.connect(self.onReadyRead)  # 准备读取信号
        self._conn.error.connect(self.onError)  # 连接错误信号
        self._conn.connectToHost(self.HOST, self.PORT)

    def onConnected(self):
        """连接成功"""
        self.buttonConnect.setEnabled(False)  # 按钮不可用
        # 设置初始拉动条可用
        self.sliderForward.setEnabled(True)
        self.sliderBackward.setEnabled(True)
        self.sliderLeft.setEnabled(True)
        self.sliderRight.setEnabled(True)
        self.browserResult.append('连接成功')  # 记录日志

    def onDisconnected(self):
        """丢失连接"""
        self.buttonConnect.setEnabled(True)  # 按钮可用
        # 设置初始拉动条不可用
        self.sliderForward.setEnabled(False)
        self.sliderBackward.setEnabled(False)
        self.sliderLeft.setEnabled(False)
        self.sliderRight.setEnabled(False)
        # 把数据设置为最小值
        self.sliderForward.setValue(self.sliderForward.minimum())
        self.sliderBackward.setValue(self.sliderBackward.minimum())
        self.sliderLeft.setValue(self.sliderLeft.minimum())
        self.sliderRight.setValue(self.sliderRight.minimum())
        self.browserResult.append('丢失连接')  # 记录日志

    def onReadyRead(self):
        """接收到数据"""
        while self._conn.bytesAvailable() > 0:
            try:
                data = self._conn.readAll().data()
                self.browserResult.append('接收到数据: ' + data.decode())
            except Exception as e:
                self.browserResult.append('解析数据错误: ' + str(e))

    def onError(self, _):
        """连接报错"""
        self.buttonConnect.setEnabled(True)  # 按钮可用
        self.browserResult.append('连接服务器错误: ' + self._conn.errorString())

    def doForward(self, value):
        """向前"""
        # 发送的内容为  F:1 类似的
        self.sendData('F:', str(value))

    def doBackward(self, value):
        """向后"""
        # 发送的内容为  B:1 类似的
        self.sendData('B:', str(value))

    def doLeft(self, value):
        """向左"""
        # 发送的内容为  L:1 类似的
        self.sendData('L:', str(value))

    def doRight(self, value):
        """向右"""
        # 发送的内容为  R:1 类似的
        self.sendData('R:', str(value))

    def sendData(self, ver, data):
        """发送数据"""
        if not self._conn or not self._conn.isWritable():
            return self.browserResult.append('服务器未连接或不可写入数据')
#         self._conn.write(ver.encode() + str(data).encode())

        # 我的服务器需要接收以\n结尾的数据
        self._conn.write(ver.encode() + str(data).encode() + b'\n')


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = ControlCar()
    w.show()
    sys.exit(app.exec_())
