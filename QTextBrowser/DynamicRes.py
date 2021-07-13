#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/6/3
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: DynamicRes
@description: 
"""
from threading import Thread

import requests

try:
    from PyQt5.QtCore import QUrl, QByteArray
    from PyQt5.QtGui import QImage, QTextDocument
    from PyQt5.QtWidgets import QApplication, QTextBrowser, QWidget, QVBoxLayout, QPushButton
except ImportError:
    from PySide2.QtCore import QUrl, QByteArray
    from PySide2.QtGui import QImage, QTextDocument
    from PySide2.QtWidgets import QApplication, QTextBrowser, QWidget, QVBoxLayout, QPushButton


class TextBrowser(QTextBrowser):
    NetImages = {}

    def __init__(self, *args, **kwargs):
        super(TextBrowser, self).__init__(*args, **kwargs)
        self.setOpenLinks(False)  # 禁止打开URL

    def downloadImage(self, url):
        try:
            self.NetImages[url] = [QByteArray(requests.get(url.toString()).content), 1]
            print('下载完成', url)
        except Exception as e:
            print('下载失败', url, e)
            self.NetImages[url] = [QByteArray(), 1]

    def loadResource(self, rtype, url):
        ret = super(TextBrowser, self).loadResource(rtype, url)
        # 加载图片资源
        if rtype == QTextDocument.ImageResource:
            if ret:
                return ret
            if url.toString().startswith('irony'):  # 自定义的协议头
                print('加载本地', '../Donate/zhifubao.png', url)
                return QImage(
                    '../Donate/zhifubao.png')  # 或者 QByteArray(open('../Donate/zhifubao.png', 'rb').read())
            elif url.toString().startswith('http'):  # 加载网络图片
                img, status = self.NetImages.get(url, [None, None])
                if url not in self.NetImages or status is None:
                    # 子线程下载
                    self.NetImages[url] = [None, 1]
                    print('download ', url)
                    Thread(target=self.downloadImage, args=(url,), daemon=True).start()
                elif img:
                    return img
        return ret

    def mouseDoubleClickEvent(self, event):
        # 双击图片得到图片的URL，也可以用来放大显示
        super(TextBrowser, self).mouseDoubleClickEvent(event)
        url = self.anchorAt(event.pos())
        if url:
            print('url:', url, self.document().resource(QTextDocument.ImageResource, QUrl(url)))


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        self.textBrowser = TextBrowser(self)
        self.downButton = QPushButton('加载网络图片', self)

        layout.addWidget(self.textBrowser)
        layout.addWidget(self.downButton)

        # 加载本地图片
        img = QImage('../Donate/weixin.png')
        # 第二个参数为任意唯一的url类似于qrc方式
        self.textBrowser.document().addResource(QTextDocument.ImageResource,
                                                QUrl('dynamic:/images/weixin.png'), img)

        # 设置html
        # 需要注意里面的图片地址
        self.textBrowser.setHtml(
            '<p><a href="../Donate/weixin.png"><img src="../Donate/weixin.png"></a></p>'  # 方式一直接加载本地图片
            '<p><a href="dynamic:/images/weixin.png"><img src="dynamic:/images/weixin.png"></a></p>'  # 方式二通过addResource添加资源
            '<p><a href="irony://zhifubao.png"><img src="irony://zhifubao.png"></a></p>'  # 方式三定义自定义的协议头通过loadResource动态加载
            '<p><a href="https://blog.pyqt.site/img/avatar.png"><img '  # 方式四类似方式三，只不过需要从网络中下载
            'src="https://blog.pyqt.site/img/avatar.png"></a></p>')


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
