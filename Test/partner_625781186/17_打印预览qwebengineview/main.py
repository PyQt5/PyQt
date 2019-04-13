
"""  QWebEngineView in QPrintPreviewDialog"""
"""
Created on 2019-01-17 <br>
description: 摘抄自 eric6 和 https://github.com/pandel/opsiPackageBuilder/blob/c0e660ecc8d4ec8fb8dc242d2174490c5dc67930/oPB/gui/utilities.py <br>
author: 625781186@qq.com <br>
site: https://github.com/625781186 <br>
更多经典例子:https://github.com/892768447/PyQt <br>
课件: https://github.com/625781186/WoHowLearn_PyQt5 <br>
视频教程: https://space.bilibili.com/1863103/#/ <br>
"""
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineWidgets import *
import sys


class HtmlView(QWebEngineView):
    """Subclass QWebView and connect to a QPrintPreviewDialog object"""

    def __init__(self, url="", parent=None, ):
        """
        Constructor of HtmlView
        :param parent: parent of the view
        :param url: url to load, if set, a loadFInished signal is emitted
        """
        super().__init__(parent)

        self.html = ""
        self.setUrl(QUrl(url))

        self.preview = QPrintPreviewDialog()

        self.textedit = QTextEdit()

        self.preview.paintRequested.connect(self.printPreview)

        if url != "":
            self.loadFinished.connect(self.execpreview)

    def execpreview(self, arg):
        self.preview.exec()

    # -------------法一------------- ↓
    ## 通过将Html 写到textedit , 再将textedit渲染到printpreviewdialog
    # def execpreview(self, arg):
    #     self.page().toHtml(self.setHtml_)
    #     self.preview.exec()
    #
    # def printPreview(self, printer):
    #
    #     self.textedit.print(printer)
    #
    # def setHtml_(self, html):
    #
    #     self.textedit.setHtml(html)
    #
    #     # small workaround to find the QPrintPreviewWidget inside the pre-defined dialog and force it to update its content
    #     wdg = self.preview.findChild(QPrintPreviewWidget)
    #     if wdg is not None:
    #         wdg.updatePreview()
    # -------------法一------------- ↑

    def printPreview(self, printer):
        # 打印机颜色
        printer.setColorMode(QPrinter.GrayScale)
        # 起始页?
        printer.setPageOrder(QPrinter.FirstPageFirst)
        # 页边距
        printer.setPageMargins(
            1.0 * 10, 1.0 * 10, 1.0 * 10, 1.0 * 10,
            QPrinter.Millimeter
        )
        # 文档名
        # printer.setPrinterName("打印机里显示的文档名")
        # 设置DPI
        printer.setResolution(150)
        # ----------------------------------------------
        ## !需要开启事件循环 , 否则无法渲染到 printpreviewdialog
        loop = QEventLoop()
        QTimer.singleShot(10000, loop.quit)

        self.page().print(printer,
                          lambda *a: loop.quit() if loop and loop.isRunning() else None)

        loop.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = HtmlView(url="file:///报警记录2019-04-12 16-52-53.html")

    main_window.show()
    app.exec_()
