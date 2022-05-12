#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2022/05/12
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: SetCookies.py
@description: 主动设置Cookie
"""

try:
    from PyQt5.QtCore import QDateTime, Qt, QUrl
    from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineView
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtNetwork import QNetworkCookie
except ImportError:
    from PySide2.QtCore import QDateTime, Qt, QUrl
    from PySide2.QtWebEngineWidgets import QWebEngineProfile, QWebEngineView
    from PySide2.QtWidgets import QApplication
    from PySide2.QtNetwork import QNetworkCookie

cookies = [{
    "domain": "pyqt.site",
    "expirationDate": 1714906174.734258,
    "hostOnly": True,
    "httpOnly": False,
    "name": "snexid",
    "path": "/",
    "sameSite": None,
    "secure": False,
    "session": False,
    "storeId": None,
    "value": "1-22-333-4444-55555"
}, {
    "domain": "pyqt.site",
    "expirationDate": 1714906174.734258,
    "hostOnly": True,
    "httpOnly": True,
    "name": "testonly",
    "path": "/",
    "secure": True,
    "value": "testonly"
}, {
    "domain": "pyqt.site",
    "hostOnly": True,
    "httpOnly": False,
    "name": "test",
    "path": "/",
    "secure": False,
    "value": "test"
}]


class Window(QWebEngineView):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # global
        # self.cookieStore = QWebEngineProfile.defaultProfile().cookieStore()

        # current
        self.cookieStore = self.page().profile().cookieStore()
        self.initCookies()
        self.loadProgress.connect(self.onLoadProgress)
        self.load(QUrl('https://pyqt.site'))

    def onLoadProgress(self, progress):
        if progress == 100:
            # 测试获取cookie
            self.page().runJavaScript('alert(document.cookie);')

    def initCookies(self):
        for cookie in cookies:
            qcookie = QNetworkCookie()
            qcookie.setName(cookie.get('name', '').encode())
            qcookie.setValue(cookie.get('value', '').encode())
            qcookie.setDomain(cookie.get('domain', ''))
            qcookie.setPath(cookie.get('path', ''))
            qcookie.setExpirationDate(
                QDateTime.fromString(str(cookie.get('expirationDate', 0)),
                                     Qt.ISODate))
            qcookie.setHttpOnly(cookie.get('httpOnly', False))
            qcookie.setSecure(cookie.get('secure', False))
            # 注意可以设置具体的url
            self.cookieStore.setCookie(qcookie, QUrl())


if __name__ == '__main__':
    import cgitb
    import sys

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
