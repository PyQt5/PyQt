#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年12月20日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ChatWidget
@description: 
"""
import json
import os
import sys
from collections import OrderedDict

import chardet
from PyQt5.Qsci import QsciScintilla, QsciLexerJSON
from PyQt5.QtChart import QChartView
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QKeySequence, QMovie
from PyQt5.QtWidgets import QSplitter, QTreeWidget, QApplication, QWidget, \
    QVBoxLayout, QPushButton, QTreeWidgetItem, QMessageBox, QShortcut, QLabel

from ChartView import ChartView  # @UnresolvedImport


class LoadingWidget(QLabel):

    def __init__(self, *args, **kwargs):
        super(LoadingWidget, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self._movie = QMovie("loading.gif")
        self.setMovie(self._movie)

    def deleteLater(self):
        self._movie.stop()
        self._movie.deleteLater()
        del self._movie
        super(LoadingWidget, self).deleteLater()

    def show(self):
        self.setVisible(True)
        super(LoadingWidget, self).show()
        self._movie.start()

    def closeEvent(self, event):
        self._movie.stop()
        self.setVisible(False)
        super(LoadingWidget, self).closeEvent(event)


class ClassifyWidget(QTreeWidget):
    fileSelected = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(ClassifyWidget, self).__init__(*args, **kwargs)
        self.setHeaderHidden(True)
        self.setColumnCount(1)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)
        baseDir = "分类"
        for name in os.listdir(baseDir):
            path = os.path.join(baseDir, name)
            if os.path.isdir(path):
                item = QTreeWidgetItem(self)
                item.setText(0, name)
                for file in os.listdir(path):
                    path = os.path.join(path, file)
                    if os.path.isfile(path) and file.endswith(".json"):
                        item = QTreeWidgetItem(item)
                        item.setText(0, os.path.splitext(file)[0])
                        item.setToolTip(0, path)
        self.expandAll()

    def onItemDoubleClicked(self, item):
        file = item.toolTip(0)
        if file:
            self.fileSelected.emit(file)


class CodeScintilla(QsciScintilla):

    def __init__(self, *args, **kwargs):
        super(CodeScintilla, self).__init__(*args, **kwargs)
        self.init()
        self.linesChanged.connect(self.onLinesChanged)

    def onLinesChanged(self):
        self.setMarginWidth(0, self.fontMetrics().width(str(self.lines())) + 6)

    def init(self):
        self.setUtf8(True)
        lexer = QsciLexerJSON(self)
        self.setLexer(lexer)
        self.setAutoCompletionCaseSensitivity(False)  # 忽略大小写
        self.setAutoCompletionSource(self.AcsAll)
        self.setAutoCompletionThreshold(1)  # 一个字符就弹出补全
        self.setAutoIndent(True)  # 自动缩进
        self.setBackspaceUnindents(True)
        self.setBraceMatching(self.StrictBraceMatch)
        self.setIndentationGuides(True)
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setTabIndents(True)
        self.setTabWidth(4)
        self.setWhitespaceSize(1)
        self.setWhitespaceVisibility(self.WsVisible)
        self.setWhitespaceForegroundColor(Qt.gray)
        self.setWrapIndentMode(self.WrapIndentFixed)
        self.setWrapMode(self.WrapWord)
        # 折叠
        self.setFolding(self.BoxedTreeFoldStyle, 2)
        self.setFoldMarginColors(QColor("#676A6C"), QColor("#676A6D"))
        font = self.font() or QFont()
        font.setFamily("Consolas")
        font.setFixedPitch(True)
        font.setPointSize(13)
        self.setFont(font)
        self.setMarginsFont(font)
        self.fontmetrics = QFontMetrics(font)
        lexer.setFont(font)
        self.setMarginWidth(0, self.fontmetrics.width(str(self.lines())) + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("gainsboro"))
        self.setMarginWidth(1, 0)
        self.setMarginWidth(2, 14)  # 折叠区域
        # 绑定自动补齐热键Alt+/
        completeKey = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Slash), self)
        completeKey.setContext(Qt.WidgetShortcut)
        completeKey.activated.connect(self.autoCompleteFromAll)


class CodeWidget(QWidget):
    runSignal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(CodeWidget, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.runButton = QPushButton(
            "运行", self, objectName="RunButton", clicked=self.onRunButton)
        self.codeScintilla = CodeScintilla(self)
        layout.addWidget(self.runButton)
        layout.addWidget(self.codeScintilla)

    def onRunButton(self):
        text = self.text()
        if not text:
            return QMessageBox.information(self, "提示", "json数据不能为空")
        self.runSignal.emit(text)

    def openFile(self, file):
        try:
            with open(file, "rb") as fp:
                text = fp.read()
                encoding = chardet.detect(text) or {}
                encoding = encoding.get(
                    "encoding", "utf-8") or "utf-8"
                text = text.decode(encoding)
                try:
                    text = json.dumps(
                        json.loads(text, encoding=encoding,
                                   object_pairs_hook=OrderedDict),
                        ensure_ascii=False, indent=4)
                except Exception as e:
                    print(e)
                self.setText(text)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def setText(self, text):
        self.codeScintilla.setText(text)

    def text(self):
        return self.codeScintilla.text().strip()


class ChartWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(ChartWidget, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self)
        layout.addWidget(self.splitter)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 3)
        self.splitter.setStretchFactor(2, 5)
        self.splitter.setAutoFillBackground(True)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setHandleWidth(2)
        # 分类
        self.classifyWidget = ClassifyWidget(self)
        self.splitter.addWidget(self.classifyWidget)
        # 代码
        self.codeWidget = CodeWidget(self)
        self.splitter.addWidget(self.codeWidget)

        # 等待界面
        self.loadingWidget = LoadingWidget(self, visible=False)
        self.loadingWidget.resize(self.size())

        # 绑定信号槽
        self.classifyWidget.fileSelected.connect(self.codeWidget.openFile)
        self.codeWidget.runSignal.connect(self.onRun)

    def onRun(self, text):
        self.setEnabled(False)
        self.loadingWidget.show()
        # 解析json生成view并添加
        if hasattr(self, "previewView"):
            # 删除旧view
            self.previewView.setParent(None)
            self.previewView.setVisible(False)
            self.previewView.hide()
            self.previewView.deleteLater()
            del self.previewView
        self.previewView = self.getChartView(text)
        if isinstance(self.previewView, QChartView):
            self.splitter.addWidget(self.previewView)
        else:
            QMessageBox.warning(self, "提示", self.previewView)
            del self.previewView
        self.setEnabled(True)
        self.loadingWidget.close()

    def getChartView(self, text):
        try:
            return ChartView(text)
        except Exception as e:
            return str(e)

    def resizeEvent(self, event):
        super(ChartWidget, self).resizeEvent(event)
        self.loadingWidget.resize(self.size())

    def closeEvent(self, event):
        self.loadingWidget.close()
        self.loadingWidget.deleteLater()
        del self.loadingWidget
        super(ChartWidget, self).closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ChartWidget()
    w.show()
    sys.exit(app.exec_())
