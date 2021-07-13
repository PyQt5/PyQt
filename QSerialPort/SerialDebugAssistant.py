#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月6日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: SerialDebugAssistant
@description: 串口调试小助手
"""
from PyQt5.QtCore import pyqtSlot, QIODevice, QByteArray
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
from PyQt5.QtWidgets import QWidget, QMessageBox

from Lib.UiSerialPort import Ui_FormSerialPort  # @UnresolvedImport


class Window(QWidget, Ui_FormSerialPort):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._serial = QSerialPort(self)  # 用于连接串口的对象
        self._serial.readyRead.connect(self.onReadyRead)  # 绑定数据读取信号
        # 首先获取可用的串口列表
        self.getAvailablePorts()

    @pyqtSlot()
    def on_buttonConnect_clicked(self):
        # 打开或关闭串口按钮
        if self._serial.isOpen():
            # 如果串口是打开状态则关闭
            self._serial.close()
            self.textBrowser.append('串口已关闭')
            self.buttonConnect.setText('打开串口')
            self.labelStatus.setProperty('isOn', False)
            self.labelStatus.style().polish(self.labelStatus)  # 刷新样式
            return

        # 根据配置连接串口
        name = self.comboBoxPort.currentText()
        if not name:
            QMessageBox.critical(self, '错误', '没有选择串口')
            return
        port = self._ports[name]
        #         self._serial.setPort(port)
        # 根据名字设置串口（也可以用上面的函数）
        self._serial.setPortName(port.systemLocation())
        # 设置波特率
        self._serial.setBaudRate(  # 动态获取,类似QSerialPort::Baud9600这样的吧
            getattr(QSerialPort, 'Baud' + self.comboBoxBaud.currentText()))
        # 设置校验位
        self._serial.setParity(  # QSerialPort::NoParity
            getattr(QSerialPort, self.comboBoxParity.currentText() + 'Parity'))
        # 设置数据位
        self._serial.setDataBits(  # QSerialPort::Data8
            getattr(QSerialPort, 'Data' + self.comboBoxData.currentText()))
        # 设置停止位
        self._serial.setStopBits(  # QSerialPort::Data8
            getattr(QSerialPort, self.comboBoxStop.currentText()))

        # NoFlowControl          没有流程控制
        # HardwareControl        硬件流程控制(RTS/CTS)
        # SoftwareControl        软件流程控制(XON/XOFF)
        # UnknownFlowControl     未知控制
        self._serial.setFlowControl(QSerialPort.NoFlowControl)
        # 读写方式打开串口
        ok = self._serial.open(QIODevice.ReadWrite)
        if ok:
            self.textBrowser.append('打开串口成功')
            self.buttonConnect.setText('关闭串口')
            self.labelStatus.setProperty('isOn', True)
            self.labelStatus.style().polish(self.labelStatus)  # 刷新样式
        else:
            self.textBrowser.append('打开串口失败')
            self.buttonConnect.setText('打开串口')
            self.labelStatus.setProperty('isOn', False)
            self.labelStatus.style().polish(self.labelStatus)  # 刷新样式

    @pyqtSlot()
    def on_buttonSend_clicked(self):
        # 发送消息按钮
        if not self._serial.isOpen():
            print('串口未连接')
            return
        text = self.plainTextEdit.toPlainText()
        if not text:
            return
        text = QByteArray(text.encode('gb2312'))  # emmm windows 测试的工具貌似是这个编码
        if self.checkBoxHexSend.isChecked():
            # 如果勾选了hex发送
            text = text.toHex()
        # 发送数据
        print('发送数据:', text)
        self._serial.write(text)

    def onReadyRead(self):
        # 数据接收响应
        if self._serial.bytesAvailable():
            # 当数据可读取时
            # 这里只是简答测试少量数据,如果数据量太多了此处readAll其实并没有读完
            # 需要自行设置粘包协议
            data = self._serial.readAll()
            if self.checkBoxHexView.isChecked():
                # 如果勾选了hex显示
                data = data.toHex()
            data = data.data()
            # 解码显示（中文啥的）
            try:
                self.textBrowser.append('我收到了: ' + data.decode('gb2312'))
            except:
                # 解码失败
                self.textBrowser.append('我收到了: ' + repr(data))

    def getAvailablePorts(self):
        # 获取可用的串口
        self._ports = {}  # 用于保存串口的信息
        infos = QSerialPortInfo.availablePorts()
        infos.reverse()  # 逆序
        for info in infos:
            # 通过串口名字-->关联串口变量
            self._ports[info.portName()] = info
            self.comboBoxPort.addItem(info.portName())

    def closeEvent(self, event):
        if self._serial.isOpen():
            self._serial.close()
        super(Window, self).closeEvent(event)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
