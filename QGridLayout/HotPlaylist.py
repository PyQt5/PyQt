#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年2月4日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: TencentMovieHotPlay
@description: 
"""
import os
import sys
import webbrowser

from PyQt5.QtCore import QSize, Qt, QUrl, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QLinearGradient, QGradient, QColor, \
    QBrush, QPaintEvent, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, \
    QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea, QGridLayout, \
    QAbstractSlider
from lxml.etree import HTML  # @UnresolvedImport

# offset=0,30,60,90
Url = "http://v.qq.com/x/list/movie?pay=-1&offset={0}"

# 播放量图标
Svg_icon_play_sm = '''<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
    <path d="M10.83 8.31v.022l-4.08 2.539-.005.003-.048.03-.012-.005c-.073.051-.15.101-.246.101-.217 0-.376-.165-.413-.369l-.027-.011V5.461l.009-.005c0-.009-.009-.014-.009-.022 0-.24.197-.435.44-.435.096 0 .174.049.247.101l.031-.017 4.129 2.569v.016a.42.42 0 0 1 .153.317.418.418 0 0 1-.169.325zm3.493 2.604a.986.986 0 0 1-.948.742 1 1 0 0 1-1-1 .98.98 0 0 1 .094-.412l-.019-.01C12.79 9.559 13 8.807 13 8a5 5 0 1 0-5 5c.766 0 1.484-.186 2.133-.494l.013.03a.975.975 0 0 1 .417-.097 1 1 0 0 1 1 1 .987.987 0 0 1-.77.954A6.936 6.936 0 0 1 8 14.999a7 7 0 1 1 7-7c0 1.048-.261 2.024-.677 2.915z" fill="#999999"></path>
</svg>
'''.encode()

Svg_icon_loading = '''<svg width="100%" height="100%" viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient x1="8.042%" y1="0%" x2="65.682%" y2="23.865%" id="a">
            <stop stop-color="#03a9f4" stop-opacity="0" offset="0%"/>
            <stop stop-color="#03a9f4" stop-opacity=".631" offset="63.146%"/>
            <stop stop-color="#03a9f4" offset="100%"/>
        </linearGradient>
    </defs>
    <g fill="none" fill-rule="evenodd">
        <g transform="translate(1 1)">
            <path d="M36 18c0-9.94-8.06-18-18-18" id="Oval-2" stroke="url(#a)" stroke-width="2">
                <animateTransform
                    attributeName="transform"
                    type="rotate"
                    from="0 18 18"
                    to="360 18 18"
                    dur="0.5s"
                    repeatCount="indefinite" />
            </path>
            <circle fill="#03a9f4" cx="36" cy="18" r="4">
                <animateTransform
                    attributeName="transform"
                    type="rotate"
                    from="0 18 18"
                    to="360 18 18"
                    dur="0.5s"
                    repeatCount="indefinite" />
            </circle>
        </g>
    </g>
</svg>'''.encode()

# 主演
Actor = '''<a href="{href}" target="_blank" title="{title}" style="text-decoration: none;font-size: 12px;color: #999999;">{title}</a>&nbsp;'''


class CoverLabel(QLabel):

    def __init__(self, cover_path, cover_title, video_url, *args, **kwargs):
        super(CoverLabel, self).__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)
        self.setScaledContents(True)
        self.setMinimumSize(220, 308)
        self.setMaximumSize(220, 308)
        self.cover_path = cover_path
        self.cover_title = cover_title
        self.video_url = video_url
        self.setPixmap(QPixmap(cover_path))

    def setCoverPath(self, path):
        self.cover_path = path

    def mouseReleaseEvent(self, event):
        super(CoverLabel, self).mouseReleaseEvent(event)
        webbrowser.open_new_tab(self.video_url)

    def paintEvent(self, event):
        super(CoverLabel, self).paintEvent(event)
        if hasattr(self, "cover_title") and self.cover_title != "":
            # 底部绘制文字
            painter = QPainter(self)
            rect = self.rect()
            # 粗略字体高度
            painter.save()
            fheight = self.fontMetrics().height()
            # 底部矩形框背景渐变颜色
            bottomRectColor = QLinearGradient(
                rect.width() / 2, rect.height() - 24 - fheight,
                rect.width() / 2, rect.height())
            bottomRectColor.setSpread(QGradient.PadSpread)
            bottomRectColor.setColorAt(0, QColor(255, 255, 255, 70))
            bottomRectColor.setColorAt(1, QColor(0, 0, 0, 50))
            # 画半透明渐变矩形框
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(bottomRectColor))
            painter.drawRect(rect.x(), rect.height() - 24 -
                             fheight, rect.width(), 24 + fheight)
            painter.restore()
            # 距离底部一定高度画文字
            font = self.font() or QFont()
            font.setPointSize(8)
            painter.setFont(font)
            painter.setPen(Qt.white)
            rect.setHeight(rect.height() - 12)  # 底部减去一定高度
            painter.drawText(rect, Qt.AlignHCenter |
                             Qt.AlignBottom, self.cover_title)


class ItemWidget(QWidget):

    def __init__(self, cover_path, figure_info, figure_title,
                 figure_score, figure_desc, figure_count, video_url, cover_url, img_path, *args, **kwargs):
        super(ItemWidget, self).__init__(*args, **kwargs)
        self.setMaximumSize(220, 380)
        self.setMaximumSize(220, 380)
        self.img_path = img_path
        self.cover_url = cover_url
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # 图片label
        self.clabel = CoverLabel(cover_path, figure_info, video_url, self)
        layout.addWidget(self.clabel)

        # 片名和分数
        flayout = QHBoxLayout()
        flayout.addWidget(QLabel(figure_title, self))
        flayout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        flayout.addWidget(QLabel(figure_score, self, styleSheet="color: red;"))
        layout.addLayout(flayout)

        # 主演
        layout.addWidget(
            QLabel(figure_desc, self, styleSheet="color: #999999;", openExternalLinks=True))

        # 播放量
        blayout = QHBoxLayout()
        count_icon = QSvgWidget(self)
        count_icon.setMaximumSize(16, 16)
        count_icon.load(Svg_icon_play_sm)
        blayout.addWidget(count_icon)
        blayout.addWidget(
            QLabel(figure_count, self, styleSheet="color: #999999;"))
        layout.addLayout(blayout)

    def setCover(self, path):
        self.clabel.setCoverPath(path)
        self.clabel.setPixmap(QPixmap(path))

    #         self.clabel.setText('<img src="{0}"/>'.format(os.path.abspath(path)))

    def sizeHint(self):
        # 每个item控件的大小
        return QSize(220, 380)

    def event(self, event):
        if isinstance(event, QPaintEvent):
            if event.rect().height() > 20 and hasattr(self, "clabel"):
                if self.clabel.cover_path.find("pic_v.png") > -1:  # 封面未加载
                    #                     print("start download img:", self.cover_url)
                    req = QNetworkRequest(QUrl(self.cover_url))
                    # 设置两个自定义属性方便后期reply中处理
                    req.setAttribute(QNetworkRequest.User + 1, self)
                    req.setAttribute(QNetworkRequest.User + 2, self.img_path)
                    self.parentWidget()._manager.get(req)  # 调用父窗口中的下载器下载
        return super(ItemWidget, self).event(event)


class GridWidget(QWidget):
    Page = 0
    loadStarted = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(GridWidget, self).__init__(*args, **kwargs)
        self._layout = QGridLayout(self, spacing=20)
        self._layout.setContentsMargins(20, 20, 20, 20)
        # 异步网络下载管理器
        self._manager = QNetworkAccessManager(self)
        self._manager.finished.connect(self.onFinished)

    def load(self):
        if self.Page == -1:
            return
        self.loadStarted.emit(True)
        # 延迟一秒后调用目的在于显示进度条
        QTimer.singleShot(1000, self._load)

    def _load(self):
        print("load url:", Url.format(self.Page * 30))
        url = QUrl(Url.format(self.Page * 30))
        self._manager.get(QNetworkRequest(url))

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

    def splist(self, src, length):
        # 等分列表
        return (src[i:i + length] for i in range(len(src)) if i % length == 0)

    def _parseHtml(self, html):
        #         encoding = chardet.detect(html) or {}
        #         html = html.decode(encoding.get("encoding","utf-8"))
        html = HTML(html)
        # 查找所有的li list_item
        lis = html.xpath("//li[@class='list_item']")
        if not lis:
            self.Page = -1  # 后面没有页面了
            return
        lack_count = self._layout.count() % 30  # 获取布局中上次还缺几个5行*6列的标准
        row_count = int(self._layout.count() / 6)  # 行数
        print("lack_count:", lack_count)
        self.Page += 1  # 自增+1
        if lack_count != 0:  # 上一次没有满足一行6个,需要补齐
            lack_li = lis[:lack_count]
            lis = lis[lack_count:]
            self._makeItem(lack_li, row_count)  # 补齐
            if lack_li and lis:
                row_count += 1
                self._makeItem(lis, row_count)  # 完成剩下的
        else:
            self._makeItem(lis, row_count)

    def _makeItem(self, li_s, row_count):
        li_s = self.splist(li_s, 6)
        for row, lis in enumerate(li_s):
            for col, li in enumerate(lis):
                a = li.find("a")
                video_url = a.get("href")  # 视频播放地址
                img = a.find("img")
                cover_url = "http:" + img.get("r-lazyload")  # 封面图片
                figure_title = img.get("alt")  # 电影名
                figure_info = a.find("div/span")
                figure_info = "" if figure_info is None else figure_info.text  # 影片信息
                figure_score = "".join(li.xpath(".//em/text()"))  # 评分
                # 主演
                figure_desc = "<span style=\"font-size: 12px;\">主演：</span>" + \
                              "".join([Actor.format(**dict(fd.items()))
                                       for fd in li.xpath(".//div[@class='figure_desc']/a")])
                # 播放数
                figure_count = (
                        li.xpath(".//div[@class='figure_count']/span/text()") or [""])[0]
                path = "cache/{0}.jpg".format(
                    os.path.splitext(os.path.basename(video_url))[0])
                cover_path = "Data/pic_v.png"
                if os.path.isfile(path):
                    cover_path = path
                iwidget = ItemWidget(cover_path, figure_info, figure_title,
                                     figure_score, figure_desc, figure_count, video_url, cover_url, path,
                                     self)
                self._layout.addWidget(iwidget, row_count + row, col)


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
        self.loadWidget = QSvgWidget(
            self, minimumHeight=120, minimumWidth=120, visible=False)
        self.loadWidget.load(Svg_icon_loading)

    def setLoadStarted(self, started):
        self._loadStart = started
        self.loadWidget.setVisible(started)

    def onActionTriggered(self, action):
        # 这里要判断action=QAbstractSlider.SliderMove，可以避免窗口大小改变的问题
        # 同时防止多次加载同一个url
        if action != QAbstractSlider.SliderMove or self._loadStart:
            return
        # 使用sliderPosition获取值可以同时满足鼠标滑动和拖动判断
        if self.verticalScrollBar().sliderPosition() == self.verticalScrollBar().maximum():
            # 可以下一页了
            self._widget.load()

    def resizeEvent(self, event):
        super(Window, self).resizeEvent(event)
        self.loadWidget.setGeometry(
            int((self.width() - self.loadWidget.minimumWidth()) / 2),
            int((self.height() - self.loadWidget.minimumHeight()) / 2),
            self.loadWidget.minimumWidth(),
            self.loadWidget.minimumHeight()
        )


if __name__ == "__main__":
    os.makedirs("cache", exist_ok=True)
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w._widget.load()
    sys.exit(app.exec_())
