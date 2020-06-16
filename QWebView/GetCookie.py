#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月10日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: GetCookie
@description: 
'''
import cgitb
import sys

from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication, QTextEdit


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class WebView(QWebView):

    def __init__(self, *args, **kwargs):
        super(WebView, self).__init__(*args, **kwargs)
        self.cookieView = QTextEdit()
        self.cookieView.resize(800, 400)
        self.cookieView.move(400, 400)
        self.cookieView.setWindowTitle('Cookies')
        self.cookieView.show()
        self.loadFinished.connect(self.onLoadFinished)

    def closeEvent(self, event):
        self.cookieView.close()
        super(WebView, self).closeEvent(event)

    def bytestostr(self, data):
        if isinstance(data, str):
            return data
        if isinstance(data, QByteArray):
            data = data.data()
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        else:
            data = str(data)
        return data

    def onLoadFinished(self):
        allCookies = self.page().networkAccessManager().cookieJar().allCookies()
        print("allCookies:", allCookies)
        for cookie in allCookies:
            # if cookie.domain() == ".pyqt5.com":
            self.cookieView.append(
                "domain: " + self.bytestostr(cookie.domain()))
            self.cookieView.append("path:   " + self.bytestostr(cookie.path()))
            self.cookieView.append("name:   " + self.bytestostr(cookie.name()))
            self.cookieView.append(
                "value:  " + self.bytestostr(cookie.value()))
            self.cookieView.append('')
            print("domain:", cookie.domain())
            print("path:", cookie.path())
            print("name:", cookie.name())
            print("value:", cookie.value())
            print()


if __name__ == "__main__":
    cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    w = WebView()
    w.show()
    w.load(QUrl("https://pyqt5.com"))
    sys.exit(app.exec_())
