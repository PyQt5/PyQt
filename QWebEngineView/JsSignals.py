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

try:
    from PyQt5.QtCore import QUrl, pyqtSlot, pyqtSignal
    from PyQt5.QtWebChannel import QWebChannel
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
    from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QPushButton
except ImportError:
    from PySide2.QtCore import QUrl, Slot as pyqtSlot, Signal as pyqtSignal
    from PySide2.QtWebChannel import QWebChannel
    from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
    from PySide2.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QPushButton


class WebEngineView(QWebEngineView):
    customSignal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(WebEngineView, self).__init__(*args, **kwargs)
        self.initSettings()
        self.channel = QWebChannel(self)
        # 把自身对象传递进去
        self.channel.registerObject('Bridge', self)
        # 设置交互接口
        self.page().setWebChannel(self.channel)

        # START #####以下代码可能是在5.6 QWebEngineView刚出来时的bug,必须在每次加载页面的时候手动注入
        #### 也有可能是跳转页面后就失效了，需要手动注入，有没有修复具体未测试

    #         self.page().loadStarted.connect(self.onLoadStart)
    #         self._script = open('Data/qwebchannel.js', 'rb').read().decode()

    #     def onLoadStart(self):
    #         self.page().runJavaScript(self._script)

    # END ###########################

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
        """
        eg: load("https://pyqt.site")
        :param url: 网址
        """
        return super(WebEngineView, self).load(QUrl(url))

    def initSettings(self):
        """
        eg: 初始化设置
        """
        # 获取浏览器默认设置
        settings = QWebEngineSettings.globalSettings()
        # 设置默认编码utf8
        settings.setDefaultTextEncoding("utf-8")
        # 自动加载图片,默认开启
        # settings.setAttribute(QWebEngineSettings.AutoLoadImages,True)
        # 自动加载图标,默认开启
        # settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage,True)
        # 开启js,默认开启
        # settings.setAttribute(QWebEngineSettings.JavascriptEnabled,True)
        # js可以访问剪贴板
        settings.setAttribute(
            QWebEngineSettings.JavascriptCanAccessClipboard, True)
        # js可以打开窗口,默认开启
        # settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows,True)
        # 链接获取焦点时的状态,默认开启
        # settings.setAttribute(QWebEngineSettings.LinksIncludedInFocusChain,True)
        # 本地储存,默认开启
        # settings.setAttribute(QWebEngineSettings.LocalStorageEnabled,True)
        # 本地访问远程
        settings.setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        # 本地加载,默认开启
        # settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls,True)
        # 监控负载要求跨站点脚本,默认关闭
        # settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled,False)
        # 空间导航特性,默认关闭
        # settings.setAttribute(QWebEngineSettings.SpatialNavigationEnabled,False)
        # 支持平超链接属性,默认关闭
        # settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled,False)
        # 使用滚动动画,默认关闭
        settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        # 支持错误页面,默认启用
        # settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        # 支持插件,默认关闭
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        # 支持全屏应用程序,默认关闭
        settings.setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, True)
        # 支持屏幕截屏,默认关闭
        settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
        # 支持html5 WebGl,默认开启
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        # 支持2d绘制,默认开启
        settings.setAttribute(
            QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        # 支持图标触摸,默认关闭
        settings.setAttribute(QWebEngineSettings.TouchIconsEnabled, True)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.webview = WebEngineView(self)
        layout.addWidget(self.webview)
        layout.addWidget(QPushButton(
            '发送自定义信号', self, clicked=self.webview.sendCustomSignal))

        self.webview.windowTitleChanged.connect(self.setWindowTitle)
        self.webview.load(QUrl.fromLocalFile(
            os.path.abspath('Data/JsSignals.html')))


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    # 开启F12 控制台功能，需要单独通过浏览器打开这个页面
    # 这里可以做个保护, 发布软件,启动时把这个环境变量删掉。防止他人通过环境变量开启
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '9966'
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.move(100, 100)

    # 打开调试页面
    dw = QWebEngineView()
    dw.setWindowTitle('开发人员工具')
    dw.load(QUrl('http://127.0.0.1:9966'))
    dw.move(600, 100)
    dw.show()
    sys.exit(app.exec_())
