#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/7/31
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ClipboardSlave
@description: 
"""
from PyQt5.QtCore import QUrl, pyqtSignal, QVariant, QMimeData
from PyQt5.QtRemoteObjects import QRemoteObjectNode, QRemoteObjectReplica
from PyQt5.QtWidgets import QTextBrowser


class WindowSlave(QTextBrowser):
    SignalUpdateMimeData = pyqtSignal(
        bool, QVariant,  # color
        bool, QVariant,  # html
        bool, QVariant,  # image
        bool, QVariant,  # text
        bool, QVariant,  # urls
        bool, QVariant,  # files
    )

    def __init__(self, *args, **kwargs):
        super(WindowSlave, self).__init__(*args, **kwargs)
        # 监听剪切板
        clipboard = QApplication.clipboard()
        clipboard.dataChanged.connect(self.on_data_changed)
        # 加入Master节点
        node = QRemoteObjectNode(parent=self)
        node.connectToNode(QUrl('tcp://{}:{}'.format(sys.argv[1], sys.argv[2])))
        # 获取WindowMaster对象
        self.windowMaster = node.acquireDynamic('WindowMaster')
        # 初始化成功后才能去绑定信号等
        self.windowMaster.initialized.connect(self.onInitialized)
        # 状态改变 https://doc.qt.io/qt-5/qremoteobjectreplica.html#State-enum
        self.windowMaster.stateChanged.connect(self.onStateChanged)

    def onStateChanged(self, newState, oldState):
        if newState == QRemoteObjectReplica.Suspect:
            self.append('连接丢失')

    def onInitialized(self):
        self.SignalUpdateMimeData.connect(self.windowMaster.updateMimeData)
        self.windowMaster.SignalUpdateMimeData.connect(self.updateMimeData)
        self.append('绑定信号槽完成')

    def on_data_changed(self):
        # 客户端剪贴板变化后发送到远程
        print('on_data_changed')
        clipboard = QApplication.clipboard()
        clipboard.blockSignals(True)
        mime_data = clipboard.mimeData()
        files = mime_data.data('text/uri-list')
        self.SignalUpdateMimeData.emit(
            mime_data.hasColor(), mime_data.colorData(),
            mime_data.hasHtml(), mime_data.html(),
            mime_data.hasImage(), mime_data.imageData(),
            mime_data.hasText(), mime_data.text(),
            mime_data.hasUrls(), mime_data.urls(),
            True if files else False, files,
        )
        clipboard.blockSignals(False)

    def updateMimeData(self,
                       hasColor, color,
                       hasHtml, html,
                       hasImage, image,
                       hasText, text,
                       hasUrls, urls
                       ):
        # 远程的剪贴板同步到客户端
        clipboard = QApplication.clipboard()
        clipboard.blockSignals(True)
        data = QMimeData()
        if hasColor:
            data.setColorData(color)
        if hasHtml:
            data.setHtml(html)
        if hasImage:
            data.setImageData(image)
        if hasText:
            data.setText(text)
        if hasUrls:
            data.setUrls(urls)
        clipboard.setMimeData(data)
        clipboard.blockSignals(False)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = WindowSlave()
    w.show()
    sys.exit(app.exec_())
