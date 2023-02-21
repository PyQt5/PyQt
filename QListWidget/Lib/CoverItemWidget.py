#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2023/02/22
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: CoverItemWidget.py
@description:
"""

try:
    from PyQt5.QtCore import QSize, QUrl
    from PyQt5.QtGui import QPaintEvent, QPixmap
    from PyQt5.QtNetwork import QNetworkRequest
    from PyQt5.QtWidgets import QWidget
except ImportError:
    from PySide2.QtCore import QSize, QUrl
    from PySide2.QtGui import QPaintEvent, QPixmap
    from PySide2.QtNetwork import QNetworkRequest
    from PySide2.QtWidgets import QWidget

from .Ui_CoverItemWidget import Ui_CoverItemWidget  # @UnresolvedImport


class CoverItemWidget(QWidget, Ui_CoverItemWidget):

    def __init__(self, *args, **kwargs):
        self._manager = kwargs.pop('manager', None)
        super(CoverItemWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)

    def init(self, cover_path, playlist_title, playlist_author, play_count,
             play_url, cover_url, img_path):
        self.img_path = img_path
        self.cover_url = cover_url
        # 图片label
        self.labelCover.init(cover_path, play_url, play_count)

        # 歌单
        self.labelTitle.setText(playlist_title)

        # 作者
        self.labelAuthor.setText(playlist_author)

    def setCover(self, path):
        self.labelCover.setCoverPath(path)
        self.labelCover.setPixmap(QPixmap(path))

    def sizeHint(self):
        # 每个item控件的大小
        return QSize(200, 256)

    def event(self, event):
        if isinstance(event, QPaintEvent):
            if event.rect().height() > 20 and hasattr(self, "labelCover"):
                if self.labelCover.cover_path.find("pic_v.png") > -1:  # 封面未加载
                    # print("start download img:", self.cover_url)
                    req = QNetworkRequest(QUrl(self.cover_url))
                    # 设置两个自定义属性方便后期reply中处理
                    req.setAttribute(QNetworkRequest.User + 1, self)
                    req.setAttribute(QNetworkRequest.User + 2, self.img_path)
                    if self._manager:
                        self._manager.get(req)  # 调用父窗口中的下载器下载
        return super(CoverItemWidget, self).event(event)
