#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月24日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: BlockRequest
@description: 拦截请求
"""

try:
    from PyQt5.QtCore import QUrl
    from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from PySide2.QtCore import QUrl
    from PySide2.QtWebEngineCore import QWebEngineUrlRequestInterceptor
    from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
    from PySide2.QtWidgets import QApplication


class RequestInterceptor(QWebEngineUrlRequestInterceptor):

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if url.find('pos.baidu.com') > -1 and url.find('ltu=') > -1:
            # 拦截百度联盟的广告
            print('block:', url)
            info.block(True)


class Window(QWebEngineView):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        QWebEngineProfile.defaultProfile().setRequestInterceptor(RequestInterceptor(self))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.load(QUrl('https://so.csdn.net/so/search/s.do?q=Qt&t=blog'))
    sys.exit(app.exec_())
