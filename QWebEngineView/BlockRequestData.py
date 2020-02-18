#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020年2月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: QWebEngineView.BlockRequestData
@description: 拦截请求内容
"""
from PyQt5.QtCore import QUrl, QFile, QIODevice
from PyQt5.QtWebEngineCore import QWebEngineUrlSchemeHandler,\
    QWebEngineUrlRequestInterceptor, QWebEngineUrlScheme  # @UnresolvedImport
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'
__Version__ = 'Version 1.0'


# 自定义url协议头
class UrlSchemeHandler(QWebEngineUrlSchemeHandler):

    def requestStarted(self, job):
        url = job.requestUrl().toString()
        if url == 'myurl://png':
            file = QFile('Data/app.png', job)
            file.open(QIODevice.ReadOnly)
            job.reply(b'image/png', file)

# 请求拦截器


class RequestInterceptor(QWebEngineUrlRequestInterceptor):

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        # 这里演示只是拦截所有png图片，可自由发挥比如拦截js文件，修改后再返回
        if url.endswith('.png'):
            # 原理在于重定向到自己的url协议里
            info.redirect(QUrl('myurl://png'))


class Window(QWebEngineView):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)

        # 首先获取默认的url协议
        h1 = QWebEngineUrlScheme.schemeByName(b'http')
        h2 = QWebEngineUrlScheme.schemeByName(b'https')

        # 这里需要修改增加本地文件和跨域支持
        CorsEnabled = 0x80  # 5.14才增加
        h1.setFlags(h1.flags() |
                    QWebEngineUrlScheme.SecureScheme |
                    QWebEngineUrlScheme.LocalScheme |
                    QWebEngineUrlScheme.LocalAccessAllowed |
                    CorsEnabled)
        h2.setFlags(h2.flags() |
                    QWebEngineUrlScheme.SecureScheme |
                    QWebEngineUrlScheme.LocalScheme |
                    QWebEngineUrlScheme.LocalAccessAllowed |
                    CorsEnabled)

        # 安装url拦截器和自定义url协议处理
        de = QWebEngineProfile.defaultProfile()  # @UndefinedVariable
        de.setRequestInterceptor(RequestInterceptor(self))
        de.installUrlSchemeHandler(b'myurl', UrlSchemeHandler(self))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.load(QUrl('https://www.baidu.com/'))
    sys.exit(app.exec_())
