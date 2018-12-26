#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月10日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: GetCookie
@description: 
'''
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class WebView(QWebView):

    def __init__(self, *args, **kwargs):
        super(WebView, self).__init__(*args, **kwargs)
        self.loadFinished.connect(self.onLoadFinished)

    def onLoadFinished(self):
        allCookies = self.page().networkAccessManager().cookieJar().allCookies()
        print("allCookies:", allCookies)
        for cookie in allCookies:
            # if cookie.domain() == ".pyqt5.com":
            print("domain:", cookie.domain())
            print("path:", cookie.path())
            print("name:", cookie.name())
            print("value:", cookie.value())
            print()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WebView()
    w.show()
    w.load(QUrl("https://pyqt5.com"))
    sys.exit(app.exec_())
