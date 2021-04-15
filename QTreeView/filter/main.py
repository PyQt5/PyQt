#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/8 21:31
# @Author  : 南城九叔
import base64
import json

from PyQt5.Qt import *
import cgitb

cgitb.enable(format='text')
url_role = Qt.UserRole + 1
name_role = Qt.UserRole + 2
folder_role = Qt.UserRole + 3


def get_ico(b64):
    icon = QPixmap()
    icon.loadFromData(base64.b64decode(b64))
    return icon


def _create_item(url, title, icon, folder):
    item = QStandardItem(title)
    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
    item.setData(url, url_role)
    item.setData(title, name_role)
    item.setData(folder, folder_role)
    item.setToolTip(f'{title}\n{url}')
    if icon is not None:
        item.setIcon(QIcon(get_ico(icon)))
    return item


def _create_folder_item(name1, datas, folder, icon):
    item = QStandardItem(name1)
    item.setData(name1, name_role)
    item.setData(folder, folder_role)
    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
    item.setIcon(QIcon(get_ico(icon)))
    for data in datas:
        name1 = data.get('name', '')
        url = data.get('url', '')
        items = data.get('items', [])
        icon = data.get('icon', '')
        _folder = data.get('folder', bool)
        if not _folder:
            last_item = _create_item(url, name1, icon, _folder)
            item.appendRow(last_item)
        else:
            folder_item = _create_folder_item(name1, items, _folder, icon)
            item.appendRow(folder_item)
    return item


def _create_model(parent, datas):
    model = QStandardItemModel(0, 1, parent)
    for row, data in enumerate(datas):
        name1 = data.get('name', '')
        url = data.get('url', '')
        items = data.get('items', [])
        icon = data.get('icon', '')
        folder = data.get('folder', bool)
        if not folder:
            item = _create_item(url, name1, icon, folder)
            model.appendRow(item)
        else:
            folder_item = _create_folder_item(name1, items, folder, icon)
            model.appendRow(folder_item)
    return model


class TreeView(QTreeView):

    def __init__(self):
        super().__init__()

    def hideRows(self, text):
        def hide(self, item, parent):
            n = True
            for i in range(item.rowCount()):
                _item = item.child(i)
                _index = model.indexFromItem(_item)
                if _item.data(folder_role):
                    n = hide(self, _item, _index)
                    if text in _item.text():
                        n = False
                    self.setRowHidden(i, parent, n)
                else:
                    if text in _item.text():
                        self.setRowHidden(i, parent, False)
                        n = False
                    else:
                        self.setRowHidden(i, parent, True)
            return n
        index = self.rootIndex()
        model = self.model()
        for i in range(model.rowCount()):
            item = model.item(i)
            print(item.rowCount())
            _index = model.indexFromItem(item)
            if item.data(folder_role):
                n = hide(self, item, _index)
                if text in item.text():
                    n = False
                self.setRowHidden(i, index, n)
            else:
                if text in item.text():
                    self.setRowHidden(i, index, False)
                else:
                    self.setRowHidden(i, index, True)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.seach = QLineEdit()
        layout.addWidget(self.seach)
        self.tree = TreeView()
        layout.addWidget(self.tree)
        self.setLayout(layout)
        datas = open('data.json', 'rb').read()
        self.model = _create_model(self.tree, json.loads(datas))
        self.tree.setModel(self.model)
        self.seach.textChanged.connect(self.tree.hideRows)


if __name__ == '__main__':
    app = QApplication([])
    win = Main()
    win.show()
    app.exec_()
