#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2021/12/15
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: WebChannelObject.py
@description: 交互对象，需要继承QObject并暴露接口
"""

from PyQt5.QtCore import (QJsonDocument, QJsonParseError, QObject,
                          pyqtProperty, pyqtSlot)
from PyQt5.QtNetwork import QHostAddress
from PyQt5.QtWebChannel import QWebChannel, QWebChannelAbstractTransport
from PyQt5.QtWebSockets import QWebSocketServer


class WebSocketTransport(QWebChannelAbstractTransport):

    def __init__(self, socket, *args, **kwargs):
        super(WebSocketTransport, self).__init__(*args, **kwargs)
        self.m_socket = socket
        self.m_socket.textMessageReceived.connect(self.textMessageReceived)
        self.m_socket.disconnected.connect(self.deleteLater)

    def sendMessage(self, message):
        print('sendMessage:', message)
        self.m_socket.sendTextMessage(
            QJsonDocument(message).toJson(QJsonDocument.Compact).data().decode(
                'utf-8', errors='ignore'))

    def textMessageReceived(self, message):
        print('textMessageReceived:', message)
        error = QJsonParseError()
        json = QJsonDocument.fromJson(message.encode('utf-8', errors='ignore'),
                                      error)
        if error.error:
            print('Failed to parse message:{}, Error is:{}'.format(
                message, error.errorString()))
            return
        if not json.isObject():
            print('Received JSON message that is not an object:{}'.format(
                message))
            return
        self.messageReceived.emit(json.object(), self)


class WebChannelObject(QObject):

    def __init__(self, *args, **kwargs):
        super(WebChannelObject, self).__init__(*args, **kwargs)
        # 内部属性供外部调用
        self._intValue = 0
        self._floatValue = 0.0
        self._boolValue = False
        self._strValue = ''
        # 设置数组或者字典有一定问题
        # self._listValue = []
        # self._mapValue = {}

        # webchannel对象
        self.m_webchannel = QWebChannel(self)
        # 这里默认注册自己,这里使用了类名作为名称
        self.registerObject(self.__class__.__name__, self)
        # websocket服务
        self.m_clients = {}
        self.m_server = QWebSocketServer(self.__class__.__name__,
                                         QWebSocketServer.NonSecureMode, self)

    def registerObject(self, name, obj):
        """注册对象
        @param name: 名称
        @type name: str
        @param obj: 对象
        @type obj: QObject
        """
        self.m_webchannel.registerObject(name, obj)

    def registerObjects(self, objects):
        """注册多个对象
        @param objects: 对象列表
        @type objects: list
        """
        for name, obj in objects:
            self.registerObject(name, obj)

    def deregisterObject(self, obj):
        """注销对象
        @param obj: 对象
        @type obj: QObject
        """
        self.m_webchannel.deregisterObject(obj)

    def deregisterObjects(self, objects):
        """注销多个对象
        @param objects: 对象列表
        @type objects: list
        """
        for obj in objects:
            self.deregisterObject(obj)

    def start(self, port=12345):
        """启动服务
        @param port: 端口
        @type port: int
        """
        if not self.m_server.listen(QHostAddress.Any, port):
            raise Exception(
                'Failed to create WebSocket server on port {}'.format(port))

        print('WebSocket server listening on port {}'.format(port))
        # 新连接信号
        self.m_server.newConnection.connect(self._handleNewConnection)

    def stop(self):
        """停止服务"""
        self.m_server.close()

    def _handleNewConnection(self):
        """新连接"""
        socket = self.m_server.nextPendingConnection()
        print('New WebSocket connection from {}'.format(
            socket.peerAddress().toString()))
        # 连接关闭信号
        socket.disconnected.connect(self._handleDisconnected)
        transport = WebSocketTransport(socket)
        self.m_clients[socket] = transport
        self.m_webchannel.connectTo(transport)

    def _handleDisconnected(self):
        """连接关闭"""
        socket = self.sender()
        print('WebSocket connection from {} closed'.format(
            socket.peerAddress()))
        if socket in self.m_clients:
            self.m_clients.pop(socket)
        socket.deleteLater()

    # ------- 下面是注册属性的方法 -------

    @pyqtProperty(int)
    def intValue(self):
        return self._intValue

    @intValue.setter
    def intValue(self, value):
        self._intValue = value

    @pyqtProperty(float)
    def floatValue(self):
        return self._floatValue

    @floatValue.setter
    def floatValue(self, value):
        self._floatValue = value

    @pyqtProperty(bool)
    def boolValue(self):
        return self._boolValue

    @boolValue.setter
    def boolValue(self, value):
        self._boolValue = value

    @pyqtProperty(str)
    def strValue(self):
        return self._strValue

    @strValue.setter
    def strValue(self, value):
        self._strValue = value

    # @pyqtProperty(list)
    # def listValue(self):
    #     return self._listValue

    # @listValue.setter
    # def listValue(self, value):
    #     self._listValue = value

    # @pyqtProperty(dict)
    # def mapValue(self):
    #     return self._mapValue

    # @mapValue.setter
    # def mapValue(self, value):
    #     self._mapValue = value

    # ------- 下面是注册函数的方法 -------
    # ------- 如果有返回值一定要注明 result=返回类型 -------

    @pyqtSlot(int, int, result=int)
    def testAdd(self, a, b):
        return a + b
