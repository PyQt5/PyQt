#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/7/31
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ClipboardMaster
@description: 
"""
import sys

from PyQt5.QtCore import QUrl, pyqtSlot, pyqtSignal, QLoggingCategory, QVariant, QMimeData
from PyQt5.QtRemoteObjects import QRemoteObjectHost
from PyQt5.QtWidgets import QTextBrowser


class WindowMaster(QTextBrowser):
    SignalUpdateMimeData = pyqtSignal(
        bool, QVariant,  # color
        bool, QVariant,  # html
        bool, QVariant,  # image
        bool, QVariant,  # text
        bool, QVariant,  # urls
    )

    def __init__(self, *args, **kwargs):
        super(WindowMaster, self).__init__(*args, **kwargs)
        # 监听剪切板
        clipboard = QApplication.clipboard()
        clipboard.dataChanged.connect(self.on_data_changed)
        # 开启节点
        host = QRemoteObjectHost(QUrl('tcp://0.0.0.0:' + sys.argv[1]), parent=self)
        host.enableRemoting(self, 'WindowMaster')
        self.append('开启节点完成')

    def on_data_changed(self):
        # 服务端剪贴板变化后发送到客户端
        clipboard = QApplication.clipboard()
        clipboard.blockSignals(True)
        mime_data = clipboard.mimeData()
        self.SignalUpdateMimeData.emit(
            mime_data.hasColor(), mime_data.colorData(),
            mime_data.hasHtml(), mime_data.html(),
            mime_data.hasImage(), mime_data.imageData(),
            mime_data.hasText(), mime_data.text(),
            mime_data.hasUrls(), mime_data.urls(),
        )
        clipboard.blockSignals(False)

    @pyqtSlot(
        bool, QVariant,  # color
        bool, QVariant,  # html
        bool, QVariant,  # image
        bool, QVariant,  # text
        bool, QVariant,  # urls
        bool, QVariant  # files
    )
    def updateMimeData(self,
                       hasColor, color,
                       hasHtml, html,
                       hasImage, image,
                       hasText, text,
                       hasUrls, urls,
                       hasFiles, files,
                       ):
        # 客户端剪切板同步到服务端
        self.append('收到客户端发送的剪贴板')
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
        # if hasUrls:
        #     data.setUrls(urls)
        if hasFiles:
            data.setData('')
        clipboard.setMimeData(data)
        clipboard.blockSignals(False)


if __name__ == '__main__':
    import cgitb

    cgitb.enable(format='text')
    from PyQt5.QtWidgets import QApplication

    QLoggingCategory.setFilterRules('qt.remoteobjects.debug=true\n'
                                    'qt.remoteobjects.warning=true')

    app = QApplication(sys.argv)
    w = WindowMaster()
    w.show()
    sys.exit(app.exec_())
