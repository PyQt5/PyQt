#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2025/08/08
@file: TestSerializeModel.py
@description:
"""

import json
import sys
from datetime import datetime

from Lib.qpropmapper import QPropertyMapper
from Lib.serializewidget import Ui_SerializeWidget

try:
    from PyQt5.QtCore import QRegExp, Qt
    from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat
    from PyQt5.QtWidgets import QApplication, QWidget
except ImportError:
    from PySide2.QtCore import QRegExp, Qt
    from PySide2.QtGui import QSyntaxHighlighter, QTextCharFormat
    from PySide2.QtWidgets import QApplication, QWidget


class HighlightingRule:
    def __init__(self, pattern, color):
        self.pattern = QRegExp(pattern)
        self.format = QTextCharFormat()
        self.format.setForeground(color)


class JsonHighlighter(QSyntaxHighlighter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rules = [
            # numbers
            HighlightingRule(QRegExp('([-0-9.]+)(?!([^"]*"[\\s]*\\:))'), Qt.darkRed),
            # key
            HighlightingRule(QRegExp('("[^"]*")\\s*\\:'), Qt.darkBlue),
            # value
            HighlightingRule(QRegExp(':+(?:[: []*)("[^"]*")'), Qt.darkGreen),
        ]

    def highlightBlock(self, text: str) -> None:
        for rule in self._rules:
            index = rule.pattern.indexIn(text)
            while index >= 0:
                length = rule.pattern.matchedLength()
                self.setFormat(index, length, rule.format)
                index = rule.pattern.indexIn(text, index + length)


class TestWindow(QWidget, Ui_SerializeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.resize(1200, 600)

        # json view
        self.highlighter = JsonHighlighter(self.editJsonView.document())
        self.editJsonView.textChanged.connect(self.onJsonChanged)

        # serialize model
        QPropertyMapper.Verbose = True
        self.mapper = QPropertyMapper(self)
        self.mapper.propertyChanged.connect(self.onPropertyChanged)
        self.mapper.loadData(
            {
                "input": {
                    "radioButton": True,
                    "checkBox": False,
                },
                "name": "Irony",
            }
        )

        # comboBox
        self.comboBox.addItems([f"Item {i}" for i in range(10)])

        self.mapper.bind(self.radioButton, "input.radioButton")
        self.mapper.bind(self.checkBox, "input.checkBox", True)
        self.mapper.bind(self.comboBox, "input.comboBox")
        self.mapper.bind(self.spinBox, "age")
        self.mapper.bind(self.doubleSpinBox, "money")
        self.mapper.bind(self.lineEdit, "name")

        # date and time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mapper.bind(self.timeEdit, "input.time", now)
        self.mapper.bind(self.dateEdit, "input.date", now)
        self.mapper.bind(self.dateTimeEdit, "input.dateTime", now)

        # edit
        self.mapper.bind(self.plainTextEdit, "desc.desc")
        self.mapper.bind(self.textEdit, "desc.text")

        # Correlation
        self.mapper.bind(self.spinBox_2, "correlation.slider")
        self.mapper.bind(self.horizontalSlider, "correlation.slider")
        self.mapper.bind(self.progressBar, "correlation.progress")
        self.mapper.bind(self.verticalSlider, "correlation.progress")

        # get new dict
        self.onPropertyChanged()

    def onPropertyChanged(self, *args, **kwargs):
        data = self.mapper.toJson(indent=2)
        self.editJsonView.blockSignals(True)
        self.editJsonView.setPlainText(data)
        self.editJsonView.blockSignals(False)

    def onJsonChanged(self):
        text = self.editJsonView.toPlainText().strip()
        try:
            data = json.loads(text)
            self.mapper.loadData(data)
        except Exception:
            pass


if __name__ == "__main__":
    import cgitb
    import sys

    cgitb.enable(format="text")
    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec_())
