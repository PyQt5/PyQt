#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月27日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QWebEngineView.JsSignals
@description: 
"""
import os
from time import time

from PyQt5.QtCore import QUrl, pyqtSlot, pyqtSignal
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QPushButton


class WebView(QWebView):
    customSignal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(WebView, self).__init__(*args, **kwargs)
        self.initSettings()
        # 暴露接口对象
        self.page().mainFrame().javaScriptWindowObjectCleared.connect(self._exposeInterface)

    def _exposeInterface(self):
        """向Js暴露调用本地方法接口
        """
        self.page().mainFrame().addToJavaScriptWindowObject('Bridge', self)

    # 注意pyqtSlot用于把该函数暴露给js可以调用
    @pyqtSlot(str)
    def callFromJs(self, text):
        QMessageBox.information(self, "提示", "来自js调用：{}".format(text))

    def sendCustomSignal(self):
        # 发送自定义信号
        self.customSignal.emit('当前时间: ' + str(time()))

    @pyqtSlot(str)
    @pyqtSlot(QUrl)
    def load(self, url):
        '''
        eg: load("https://pyqt.site")
        :param url: 网址
        '''
        return super(WebView, self).load(QUrl(url))

    def initSettings(self):
        '''
        eg: 初始化设置
        '''
        # 获取浏览器默认设置
        settings = self.settings()
        # 开启开发人员工具
        settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        # 设置默认编码
        settings.setDefaultTextEncoding('UTF-8')


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.webview = WebView(self)
        layout.addWidget(self.webview)
        layout.addWidget(QPushButton(
            '发送自定义信号', self, clicked=self.webview.sendCustomSignal))

        self.webview.windowTitleChanged.connect(self.setWindowTitle)
        self.webview.load(QUrl.fromLocalFile(
            os.path.abspath('Data/JsSignals.html')))


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.move(100, 100)
    sys.exit(app.exec_())
