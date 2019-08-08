#!/usr/bin/python


#############################################################################
##
## Copyright (C) 2018 Riverbank Computing Limited
## Copyright (C) 2017 Ford Motor Company
##
## This file is part of the PyQt examples.
##
## $QT_BEGIN_LICENSE:BSD$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## BSD License Usage
## Alternatively, you may use this file under the terms of the BSD license
## as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


import sys

from PyQt5.QtCore import (pyqtSlot, QLoggingCategory, QModelIndex, QObject, Qt,
        QTimer, QUrl)
from PyQt5.QtGui import QColor, QStandardItem, QStandardItemModel
from PyQt5.QtRemoteObjects import QRemoteObjectHost, QRemoteObjectRegistryHost
from PyQt5.QtWidgets import QApplication, QTreeView


class TimerHandler(QObject):

    def __init__(self, model, parent=None):
        super().__init__(parent)

        self._model = model

    @pyqtSlot()
    def changeData(self):
        for i in range(10, 50):
            self._model.setData(self._model.index(i, 1), QColor(Qt.blue),
                    Qt.BackgroundRole)

    @pyqtSlot()
    def insertData(self):
        self._model.insertRows(2, 9)

        for i in range(2, 11):
            self._model.setData(self._model.index(i, 1), QColor(Qt.green),
                    Qt.BackgroundRole)
            self._model.setData(self._model.index(i, 1), "InsertedRow",
                    Qt.DisplayRole)

    @pyqtSlot()
    def removeData(self):
        self._model.removeRows(2, 4)

    @pyqtSlot()
    def changeFlags(self):
        item = self._model.item(0, 0)
        item.setEnabled(False)

        item = item.child(0, 0)
        item.setFlags(item.flags() & Qt.ItemIsSelectable)

    @pyqtSlot()
    def moveData(self):
        self._model.moveRows(QModelIndex(), 2, 4, QModelIndex(), 10)


def addChild(numChildren, nestingLevel):
    result = []

    if nestingLevel == 0:
        return result

    for i in range(numChildren):
        child = QStandardItem(
                "Child num {}, nesting level {}".format(i + 1, nestingLevel))

        if i == 0:
            child.appendRow(addChild(numChildren, nestingLevel - 1))

        result.append(child)

    return result


if __name__ == '__main__':

    QLoggingCategory.setFilterRules('qt.remoteobjects.debug=false\n'
                                    'qt.remoteobjects.warning=false')

    app = QApplication(sys.argv)

    sourceModel = QStandardItemModel()
    sourceModel.setHorizontalHeaderLabels(
            ["First Column with spacing", "Second Column with spacing"])

    for i in range(10000):
        firstItem = QStandardItem("FancyTextNumber {}".format(i))
        if i == 0:
            firstItem.appendRow(addChild(2, 2))

        secondItem = QStandardItem("FancyRow2TextNumber {}".format(i))
        if i % 2 == 0:
            firstItem.setBackground(Qt.red)

        sourceModel.invisibleRootItem().appendRow([firstItem, secondItem])

    # Needed by QMLModelViewClient.
    roleNames = {
        Qt.DisplayRole: b'_text',
        Qt.BackgroundRole: b'_color'
    }
    sourceModel.setItemRoleNames(roleNames)

    roles = [Qt.DisplayRole, Qt.BackgroundRole]

    node = QRemoteObjectRegistryHost(QUrl('local:registry'))

    node2 = QRemoteObjectHost(QUrl('local:replica'), QUrl('local:registry'))
    node2.enableRemoting(sourceModel, 'RemoteModel', roles)

    view = QTreeView()
    view.setWindowTitle("SourceView")
    view.setModel(sourceModel)
    view.show()

    handler = TimerHandler(sourceModel)
    QTimer.singleShot(5000, handler.changeData)
    QTimer.singleShot(10000, handler.insertData)
    QTimer.singleShot(11000, handler.changeFlags)
    QTimer.singleShot(12000, handler.removeData)
    QTimer.singleShot(13000, handler.moveData)

    sys.exit(app.exec_())
