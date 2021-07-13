#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月8日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ScreenShotPage
@description: 网页整体截图
"""
import base64
import cgitb
import os
import sys

try:
    from PyQt5.QtCore import QUrl, Qt, pyqtSlot, QSize, QTimer, QPoint
    from PyQt5.QtGui import QImage, QPainter, QIcon, QPixmap
    from PyQt5.QtWebChannel import QWebChannel
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
    from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
        QGroupBox, QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem, \
        QProgressDialog
except ImportError:
    from PySide2.QtCore import QUrl, Qt, Slot as pyqtSlot, QSize, QTimer, QPoint
    from PySide2.QtGui import QImage, QPainter, QIcon, QPixmap
    from PySide2.QtWebChannel import QWebChannel
    from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
    from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
        QGroupBox, QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem, \
        QProgressDialog

# 对部分内容进行截图
CODE = """
var el = $("%s");
html2canvas(el[0], {
    width: el.outerWidth(true), 
    windowWidth: el.outerWidth(true),
}).then(function(canvas) {
    window._self.saveImage(canvas.toDataURL());
    canvas = null;
});
"""

# 创建交互桥梁脚本
CreateBridge = """
new QWebChannel(qt.webChannelTransport,
    function(channel) {
        window._self = channel.objects._self;
    }
);
"""


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(600, 400)
        layout = QHBoxLayout(self)

        # 左侧
        widgetLeft = QWidget(self)
        layoutLeft = QVBoxLayout(widgetLeft)
        # 右侧
        self.widgetRight = QListWidget(
            self, minimumWidth=200, iconSize=QSize(150, 150))
        self.widgetRight.setViewMode(QListWidget.IconMode)
        layout.addWidget(widgetLeft)
        layout.addWidget(self.widgetRight)

        self.webView = QWebEngineView()
        layoutLeft.addWidget(self.webView)

        # 截图方式一
        groupBox1 = QGroupBox('截图方式一', self)
        layout1 = QVBoxLayout(groupBox1)
        layout1.addWidget(QPushButton('截图1', self, clicked=self.onScreenShot1))
        layoutLeft.addWidget(groupBox1)

        # 截图方式二（采用js）
        groupBox2 = QGroupBox('截图方式二', self)
        layout2 = QVBoxLayout(groupBox2)
        self.codeEdit = QLineEdit(
            'body', groupBox2, placeholderText='请输入需要截图的元素、ID或者class：如body、#id .class')
        layout2.addWidget(self.codeEdit)
        self.btnMethod2 = QPushButton(
            '', self, clicked=self.onScreenShot2, enabled=False)
        layout2.addWidget(self.btnMethod2)
        layoutLeft.addWidget(groupBox2)

        # 提供访问接口
        self.channel = QWebChannel(self)
        # 把自身对象传递进去
        self.channel.registerObject('_self', self)
        # 设置交互接口
        self.webView.page().setWebChannel(self.channel)
        # 支持截图
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
        self.webView.loadStarted.connect(self.onLoadStarted)
        self.webView.loadFinished.connect(self.onLoadFinished)
        self.webView.load(QUrl("https://pyqt.site"))

    def onLoadStarted(self):
        print('load started')
        self.btnMethod2.setEnabled(False)
        self.btnMethod2.setText('暂时无法使用（等待页面加载完成）')

    @pyqtSlot(bool)
    def onLoadFinished(self, finished):
        if not finished:
            return
        print('load finished')
        # 注入脚本
        page = self.webView.page()
        # 执行qwebchannel,jquery,promise,html2canvas
        page.runJavaScript(
            open('Data/qwebchannel.js', 'rb').read().decode())
        page.runJavaScript(
            open('Data/jquery.js', 'rb').read().decode())
        #         page.runJavaScript(
        #             open('Data/promise-7.0.4.min.js', 'rb').read().decode())
        page.runJavaScript(
            open('Data/html2canvas.min.js', 'rb').read().decode())
        page.runJavaScript(CreateBridge)
        print('inject js ok')
        self.btnMethod2.setText('截图2')
        self.btnMethod2.setEnabled(True)

    def onScreenShot1(self):
        # 截图方式1
        page = self.webView.page()
        oldSize = self.webView.size()
        self.webView.resize(page.contentsSize().toSize())

        def doScreenShot():
            rect = self.webView.contentsRect()
            size = rect.size()
            image = QImage(size, QImage.Format_ARGB32_Premultiplied)
            image.fill(Qt.transparent)

            painter = QPainter()
            painter.begin(image)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            self.webView.render(painter, QPoint())
            painter.end()
            self.webView.resize(oldSize)

            # 添加到左侧list中
            item = QListWidgetItem(self.widgetRight)
            image = QPixmap.fromImage(image)
            item.setIcon(QIcon(image))
            item.setData(Qt.UserRole + 1, image)

        # 先等一下再截图吧
        QTimer.singleShot(2000, doScreenShot)

    def onScreenShot2(self):
        # 截图方式2
        code = self.codeEdit.text().strip()
        if not code:
            return
        self.progressdialog = QProgressDialog(self, windowTitle='正在截图中')
        self.progressdialog.setRange(0, 0)
        self.webView.page().runJavaScript(CODE % code)
        self.progressdialog.exec_()

    @pyqtSlot(str)
    def saveImage(self, image):
        self.progressdialog.close()
        # data:image/png;base64,iVBORw0KG....
        if not image.startswith('data:image'):
            return
        data = base64.b64decode(image.split(';base64,')[1])
        image = QPixmap()
        image.loadFromData(data)
        # 添加到左侧list中
        item = QListWidgetItem(self.widgetRight)
        item.setIcon(QIcon(image))
        item.setData(Qt.UserRole + 1, image)


if __name__ == '__main__':
    # 开启F12 控制台功能，需要单独通过浏览器打开这个页面
    # 这里可以做个保护, 发布软件,启动时把这个环境变量删掉。防止他人通过环境变量开启
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '9966'
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    w = Window()
    w.show()

    # 打开调试页面
    dw = QWebEngineView()
    dw.setWindowTitle('开发人员工具')
    dw.load(QUrl('http://127.0.0.1:9966'))
    dw.show()
    dw.move(100, 100)
    sys.exit(app.exec_())
