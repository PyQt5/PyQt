#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月24日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QWebEngineView.BlockAds
@description: 拦截请求
"""

try:
    from PyQt5.QtCore import QUrl, QByteArray
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
    from PyQt5.QtWebEngineCore import QWebEngineUrlSchemeHandler, QWebEngineUrlScheme, \
        QWebEngineUrlRequestInterceptor
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
except ImportError:
    from PySide2.QtCore import QUrl, QByteArray
    from PySide2.QtWidgets import QApplication
    from PySide2.QtNetwork import QNetworkAccessManager, QNetworkRequest
    from PySide2.QtWebEngineCore import QWebEngineUrlSchemeHandler, QWebEngineUrlScheme, \
        QWebEngineUrlRequestInterceptor
    from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile


class UrlSchemeHandler(QWebEngineUrlSchemeHandler):
    AttrType = QNetworkRequest.User + 1

    def __init__(self, *args, **kwargs):
        super(UrlSchemeHandler, self).__init__(*args, **kwargs)
        self._manager = QNetworkAccessManager(self)
        self._manager.finished.connect(self.onFinished)

    def requestStarted(self, request):
        # 拦截
        # request.fail(QWebEngineUrlRequestJob.RequestDenied)
        # print('initiator:', request.initiator())
        print('requestMethod:', request.requestMethod())
        print('requestHeaders:', request.requestHeaders())
        url = request.requestUrl()
        if url.scheme().startswith('myurl'):
            url.setScheme(url.scheme().replace('myurl', 'http'))
        print('requestUrl:', url)

        # 构造真实请求
        req = QNetworkRequest(url)
        req.setAttribute(self.AttrType, request)  # 记录
        for headerName, headerValue in request.requestHeaders().items():
            req.setRawHeader(headerName, headerValue)
        method = request.requestMethod()

        # TODO: 这里需要把浏览器内部的cookie获取出来重新设置
        if method == b'GET':
            self._manager.get(req)
        # TODO: 这里貌似没法得到POST的数据，ajax的请求貌似也有问题
        elif method == b'POST':
            self._manager.post(req)

    def onFinished(self, reply):
        req = reply.request()  # 获取请求
        o_req = req.attribute(self.AttrType, None)
        if o_req:
            # Notice: 这里可以对数据做修改再返回
            # TODO: 可能还存在 QNetworkAccessManager 与浏览器之间的 cookie 同步问题
            o_req.reply(req.header(QNetworkRequest.ContentTypeHeader) or b'text/html', reply)
            o_req.destroyed.connect(reply.deleteLater)


# 把所有请求重定向到myurl
class RequestInterceptor(QWebEngineUrlRequestInterceptor):

    def interceptRequest(self, info):
        url = info.requestUrl()
        if url.scheme() == 'http':
            # 重定向
            url.setScheme('myurl')
            info.redirect(url)
        elif url.scheme() == 'https':
            # 重定向
            url.setScheme('myurls')
            info.redirect(url)


class Window(QWebEngineView):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        profile = QWebEngineProfile.defaultProfile()

        # 首先获取默认的url协议
        o_http = QWebEngineUrlScheme.schemeByName(QByteArray(b'http'))
        o_https = QWebEngineUrlScheme.schemeByName(QByteArray(b'https'))
        print('scheme:', o_http, o_https)

        # 这里需要修改增加本地文件和跨域支持
        CorsEnabled = 0x80  # 5.14才增加
        o_http.setFlags(o_http.flags() |
                        QWebEngineUrlScheme.SecureScheme |
                        QWebEngineUrlScheme.LocalScheme |
                        QWebEngineUrlScheme.LocalAccessAllowed |
                        CorsEnabled)
        o_https.setFlags(o_https.flags() |
                         QWebEngineUrlScheme.SecureScheme |
                         QWebEngineUrlScheme.LocalScheme |
                         QWebEngineUrlScheme.LocalAccessAllowed |
                         CorsEnabled)

        # 安装url拦截器和自定义url协议处理
        de = QWebEngineProfile.defaultProfile()  # @UndefinedVariable
        de.setRequestInterceptor(RequestInterceptor(self))
        self.urlSchemeHandler = UrlSchemeHandler(self)
        de.installUrlSchemeHandler(QByteArray(b'myurl'), self.urlSchemeHandler)  # for http
        de.installUrlSchemeHandler(QByteArray(b'myurls'), self.urlSchemeHandler)  # for https


if __name__ == '__main__':
    import sys
    import os
    import webbrowser
    import cgitb

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    # 开启F12 控制台功能，需要单独通过浏览器打开这个页面
    # 这里可以做个保护, 发布软件,启动时把这个环境变量删掉。防止他人通过环境变量开启
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '9966'
    # 打开调试页面
    webbrowser.open_new_tab('http://127.0.0.1:9966')

    w = Window()
    w.show()
    w.load(QUrl('https://pyqt.site'))
    sys.exit(app.exec_())
