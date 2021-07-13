#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWidgets import QWidget


class ControlCar(QWidget):
    HOST = '127.0.0.1'
    PORT = 8888

    def __init__(self, *args, **kwargs):
        super(ControlCar, self).__init__(*args, **kwargs)
        self._connCar = None
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

        # 定时器定时向图片服务器发送请求
        self._timer = QTimer(self, timeout=self.doGetImage)

    def _clearConn(self):
        """清理连接"""
        if self._connCar:
            self._connCar.close()
            self._connCar.deleteLater()
            del self._connCar
            self._connCar = None

    def closeEvent(self, event):
        """窗口关闭事件"""
        self._timer.stop()
        self._clearConn()
        super(ControlCar, self).closeEvent(event)

    def doConnect(self):
        """连接服务器"""
        self.buttonConnect.setEnabled(False)
        self._timer.stop()
        self._clearConn()
        self.browserResult.append('正在连接服务器')
        # 连接控制小车的服务器
        self._connCar = QTcpSocket(self)
        self._connCar.connected.connect(self.onConnected)  # 绑定连接成功信号
        self._connCar.disconnected.connect(self.onDisconnected)  # 绑定连接丢失信号
        self._connCar.readyRead.connect(self.onReadyRead)  # 准备读取信号
        self._connCar.error.connect(self.onError)  # 连接错误信号
        self._connCar.connectToHost(self.HOST, self.PORT)

    def onConnected(self):
        """连接成功"""
        self.buttonConnect.setEnabled(False)  # 按钮不可用
        # 设置初始拉动条可用
        self.sliderForward.setEnabled(True)
        self.sliderBackward.setEnabled(True)
        self.sliderLeft.setEnabled(True)
        self.sliderRight.setEnabled(True)
        self.browserResult.append('连接成功')  # 记录日志
        # 开启获取摄像头图片定时器
        self._timer.start(200)

    def onDisconnected(self):
        """丢失连接"""
        self._timer.stop()
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
        while self._connCar.bytesAvailable() > 0:
            try:
                data = self._connCar.readAll().data()
                if data and data.find(b'JFIF') > -1:
                    self.qlabel.setPixmap(  # 图片
                        QPixmap.fromImage(QImage.fromData(data)))
                else:
                    self.browserResult.append('接收到数据: ' + data.decode())
            except Exception as e:
                self.browserResult.append('解析数据错误: ' + str(e))

    def onError(self, _):
        """连接报错"""
        self._timer.stop()
        self.buttonConnect.setEnabled(True)  # 按钮可用
        self.browserResult.append('连接服务器错误: ' + self._connCar.errorString())

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

    def doGetImage(self):
        # 请求图片
        self.sendData('getimage', '')

    def sendData(self, ver, data):
        """发送数据"""
        if not self._connCar or not self._connCar.isWritable():
            return self.browserResult.append('服务器未连接或不可写入数据')
        self._connCar.write(ver.encode() + str(data).encode() + b'\n')


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ControlCar()
    w.show()
    sys.exit(app.exec_())
