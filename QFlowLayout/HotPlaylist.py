#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2023/02/22
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: HotPlaylist.py
@description:
"""

import os
import sys

from Lib.CoverItemWidget import CoverItemWidget
from Lib.flowlayout import FlowLayout  # @UnresolvedImport
from lxml.etree import HTML  # @UnresolvedImport

try:
    from PyQt5.QtCore import Qt, QTimer, QUrl, pyqtSignal
    from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
    from PyQt5.QtSvg import QSvgWidget
    from PyQt5.QtWidgets import (QAbstractSlider, QApplication, QScrollArea,
                                 QWidget)
except ImportError:
    from PySide2.QtCore import Qt, QTimer, QUrl, pyqtSignal
    from PySide2.QtNetwork import QNetworkAccessManager, QNetworkRequest
    from PySide2.QtSvg import QSvgWidget
    from PySide2.QtWidgets import (QAbstractSlider, QApplication, QScrollArea,
                                   QWidget)

# offset=0,35,70,105
Url = "https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={0}"

Agent = b"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"

Referer = b"https://music.163.com"

# 作者
Actor = '''<a href="{href}" target="_blank" title="{title}" style="text-decoration: none;font-size: 12px;color: #999999;">{title}</a>&nbsp;'''


class GridWidget(QWidget):
    Page = 0
    loadStarted = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(GridWidget, self).__init__(*args, **kwargs)
        self._layout = FlowLayout(self)  # 使用自定义流式布局
        # 异步网络下载管理器
        self._manager = QNetworkAccessManager(self)
        self._manager.finished.connect(self.onFinished)

    def load(self):
        if self.Page == -1 or self.Page > 10:
            return
        self.loadStarted.emit(True)
        # 延迟一秒后调用目的在于显示进度条
        QTimer.singleShot(1000, self._load)

    def _load(self):
        print("load url:", Url.format(self.Page * 35))
        url = QUrl(Url.format(self.Page * 35))
        req = QNetworkRequest(url)
        req.setRawHeader(b"User-Agent", Agent)
        self._manager.get(req)

    def onFinished(self, reply):
        # 请求完成后会调用该函数
        req = reply.request()  # 获取请求
        iwidget = req.attribute(QNetworkRequest.User + 1, None)
        path = req.attribute(QNetworkRequest.User + 2, None)
        html = reply.readAll().data()
        reply.deleteLater()
        del reply
        if iwidget and path and html:
            # 这里是图片下载完毕
            open(path, "wb").write(html)
            iwidget.setCover(path)
            return
        # 解析网页
        self._parseHtml(html)
        self.loadStarted.emit(False)

    def _parseHtml(self, html):
        # print(html)
        #         encoding = chardet.detect(html) or {}
        #         html = html.decode(encoding.get("encoding","utf-8"))
        html = HTML(html)
        # 查找所有的li list_item
        lis = html.xpath("//ul[@id='m-pl-container']/li")
        # print(lis)
        if not lis:
            self.Page = -1  # 后面没有页面了
            return
        self.Page += 1
        self._makeItem(lis)

    def _makeItem(self, lis):
        for li in lis:
            a = li.find('.//div/a')
            play_url = "https://music.163.com" + a.get("href")  # 歌单播放地址
            img = li.find(".//div/img")
            cover_url = img.get("src")  # 封面图片
            playlist_title = a.get("title")  # 歌单名
            # 歌手
            author_info = li.xpath(".//p[2]/a")[0]
            playlist_author = "<span style=\"font-size: 12px;\"作者：{}</span>".format(
                Actor.format(href="https://music.163.com" +
                             author_info.get("href"),
                             title=author_info.get("title")))
            # 播放数
            play_count = (li.xpath(".//div/div/span[2]/text()") or [""])[0]
            path = "cache/{0}.jpg".format(
                os.path.splitext(os.path.basename(cover_url).split('?')[0])[0])
            cover_path = "Data/pic_v.png"
            if os.path.isfile(path):
                cover_path = path

            # print(cover_path, playlist_title,
            #       playlist_author, play_count, play_url, cover_url, path)
            iwidget = CoverItemWidget(self, manager=self._manager)
            iwidget.init(cover_path, playlist_title, playlist_author,
                         play_count, play_url, cover_url, path)
            self._layout.addWidget(iwidget)


class Window(QScrollArea):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setFrameShape(self.NoFrame)
        self.setWidgetResizable(True)
        self.setAlignment(Qt.AlignCenter)
        self._loadStart = False
        # 网格窗口
        self._widget = GridWidget(self)
        self._widget.loadStarted.connect(self.setLoadStarted)
        self.setWidget(self._widget)
        # 连接竖着的滚动条滚动事件
        self.verticalScrollBar().actionTriggered.connect(self.onActionTriggered)
        # 进度条
        self.loadWidget = QSvgWidget(self,
                                     minimumHeight=120,
                                     minimumWidth=120,
                                     visible=False)
        self.loadWidget.load('Data/Svg_icon_loading.svg')

    def setLoadStarted(self, started):
        self._loadStart = started
        self.loadWidget.setVisible(started)

    def onActionTriggered(self, action):
        # 这里要判断action=QAbstractSlider.SliderMove，可以避免窗口大小改变的问题
        # 同时防止多次加载同一个url
        if action != QAbstractSlider.SliderMove or self._loadStart:
            return
        # 使用sliderPosition获取值可以同时满足鼠标滑动和拖动判断
        if self.verticalScrollBar().sliderPosition() == self.verticalScrollBar(
        ).maximum():
            # 可以下一页了
            self._widget.load()

    def resizeEvent(self, event):
        super(Window, self).resizeEvent(event)
        self.loadWidget.setGeometry(
            int((self.width() - self.loadWidget.minimumWidth()) / 2),
            int((self.height() - self.loadWidget.minimumHeight()) / 2),
            self.loadWidget.minimumWidth(), self.loadWidget.minimumHeight())


if __name__ == "__main__":
    os.makedirs("cache", exist_ok=True)
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w._widget.load()
    sys.exit(app.exec_())
