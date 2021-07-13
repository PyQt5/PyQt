#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年3月30日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: 单实例应用.Application
@description: 
"""

from PyQt5.QtCore import QSharedMemory, pyqtSignal, Qt
from PyQt5.QtNetwork import QLocalSocket, QLocalServer
from PyQt5.QtWidgets import QApplication


class SharedApplication(QApplication):

    def __init__(self, *args, **kwargs):
        super(SharedApplication, self).__init__(*args, **kwargs)
        self._running = False
        key = "SharedApplication"
        self._memory = QSharedMemory(key, self)

        isAttached = self._memory.isAttached()
        print("isAttached", isAttached)
        if isAttached:  # 如果进程附加在共享内存上
            detach = self._memory.detach()  # 取消进程附加在共享内存上
            print("detach", detach)

        if self._memory.create(1) and self._memory.error() != QSharedMemory.AlreadyExists:
            # 创建共享内存，如果创建失败，则说明已经创建，否则未创建
            print("create ok")
        else:
            print("create failed")
            self._running = True
            del self._memory

    def isRunning(self):
        return self._running


class QSingleApplication(QApplication):
    messageReceived = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(QSingleApplication, self).__init__(*args, **kwargs)
        appid = QApplication.applicationFilePath().lower().split("/")[-1]
        self._socketName = "qtsingleapp-" + appid
        print("socketName", self._socketName)
        self._activationWindow = None
        self._activateOnMessage = False
        self._socketServer = None
        self._socketIn = None
        self._socketOut = None
        self._running = False

        # 先尝试连接
        self._socketOut = QLocalSocket(self)
        self._socketOut.connectToServer(self._socketName)
        self._socketOut.error.connect(self.handleError)
        self._running = self._socketOut.waitForConnected()

        if not self._running:  # 程序未运行
            self._socketOut.close()
            del self._socketOut
            self._socketServer = QLocalServer(self)
            self._socketServer.listen(self._socketName)
            self._socketServer.newConnection.connect(self._onNewConnection)
            self.aboutToQuit.connect(self.removeServer)

    def handleError(self, message):
        print("handleError message: ", message)

    def isRunning(self):
        return self._running

    def activationWindow(self):
        return self._activationWindow

    def setActivationWindow(self, activationWindow, activateOnMessage=True):
        self._activationWindow = activationWindow
        self._activateOnMessage = activateOnMessage

    def activateWindow(self):
        if not self._activationWindow:
            return
        self._activationWindow.setWindowState(
            self._activationWindow.windowState() & ~Qt.WindowMinimized)
        self._activationWindow.raise_()
        self._activationWindow.activateWindow()

    def sendMessage(self, message, msecs=5000):
        if not self._socketOut:
            return False
        if not isinstance(message, bytes):
            message = str(message).encode()
        self._socketOut.write(message)
        if not self._socketOut.waitForBytesWritten(msecs):
            raise RuntimeError("Bytes not written within %ss" %
                               (msecs / 1000.))
        return True

    def _onNewConnection(self):
        if self._socketIn:
            self._socketIn.readyRead.disconnect(self._onReadyRead)
        self._socketIn = self._socketServer.nextPendingConnection()
        if not self._socketIn:
            return
        self._socketIn.readyRead.connect(self._onReadyRead)
        if self._activateOnMessage:
            self.activateWindow()

    def _onReadyRead(self):
        while 1:
            message = self._socketIn.readLine()
            if not message:
                break
            print("Message received: ", message)
            self.messageReceived.emit(message.data().decode())

    def removeServer(self):
        self._socketServer.close()
        self._socketServer.removeServer(self._socketName)
