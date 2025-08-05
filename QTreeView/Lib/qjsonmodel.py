#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2025/08/05
@author: Irony
@site: https://pyqt.site | https://github.com/PyQt5
@email: 892768447@qq.com
@file: qjsonmodel.py
@description:
"""

import json
from typing import Any, List, Union

try:
    from PyQt5.QtCore import QObject, Qt
    from PyQt5.QtGui import QStandardItem, QStandardItemModel
except ImportError:
    from PySide2.QtCore import QObject, Qt
    from PySide2.QtGui import QStandardItem, QStandardItemModel


class QJsonItem(QStandardItem):
    Sep = "/"
    EditRole = Qt.EditRole
    KeyRole = Qt.UserRole + 1
    ValueRole = Qt.UserRole + 2
    DatasRole = Qt.UserRole + 3
    PathRole = Qt.UserRole + 4

    def __init__(
        self,
        *args,
        key: Union["QJsonItem", None] = None,  # 上一级key item
        value: Union["QJsonItem", None] = None,  # 当前value item
        editAble: bool = True,
        role: int = Qt.UserRole + 1,
    ):
        super().__init__(*args)
        self.setInfo(key, value, None, editAble, role)

    def clear(self):
        for _ in range(self.rowCount()):
            self.removeRow(0)

    def setInfo(
        self,
        key: Union["QJsonItem", None] = None,
        value: Union["QJsonItem", None] = None,
        datas: Any = None,
        editAble: bool = True,
        role: int = Qt.UserRole + 1,
        edit=None,
    ):
        self.setEditable(editAble)
        self._role = role
        self.key = key
        self.value = value
        self.edit = edit
        self.datas = datas

    @property
    def key(self) -> Any:
        # 上一级key item
        return self.data(self.KeyRole)

    @key.setter
    def key(self, value: "QJsonItem") -> None:
        self.setData(value, self.KeyRole)

    @property
    def value(self) -> Any:
        # 当前value item
        return self.data(self.ValueRole)

    @value.setter
    def value(self, value: "QJsonItem") -> None:
        self.setData(value, self.ValueRole)

    @property
    def edit(self) -> Any:
        # 设置角色为EditRole的值
        return self.data(self.EditRole)

    @edit.setter
    def edit(self, value: Any) -> None:
        if value is None:
            return
        self.setData(value, self.EditRole)

    @property
    def datas(self) -> Any:
        return self.data(self.DatasRole)

    @datas.setter
    def datas(self, value: Any) -> None:
        # key item中的原始数据设置
        self.clear()
        if self._role == QJsonItem.ValueRole:
            self.setText(f"\t[{type(value).__name__}]")
            if not isinstance(value, (list, tuple, dict)):
                self.setText(str(value))
                self.edit = value
            return
        self.setData(value, self.DatasRole)
        self.__loadData(value)

    @property
    def type(self) -> Any:
        return type(self.edit)

    @property
    def path(self) -> str:
        item = self.key if self._role == self.ValueRole else self
        paths = []

        while item:
            paths.append(item.text())
            item = item.key

        paths.reverse()
        return QJsonItem.Sep.join(paths)

    def data(self, role: int = Qt.DisplayRole) -> Any:
        if role == self.PathRole:
            return self.path

        return super().data(role)

    def __loadData(self, data: Any) -> None:
        # 数组类型的key是索引, 不允许修改
        isArray = isinstance(data, (list, tuple))
        keyEditAble = not isArray
        datas = (
            data.items()
            if isinstance(data, dict)
            else enumerate(data)
            if isArray
            else []
        )

        for key, value in datas:
            itemKey = QJsonItem(str(key))
            itemValue = QJsonItem()

            # 先添加items
            self.appendRow([itemKey, itemValue])

            itemKey.setInfo(self, itemValue, value, keyEditAble, edit=key)
            # key对应的后面的空列不允许修改
            valueEditAble = not isinstance(value, (list, tuple, dict))
            itemValue.setInfo(itemKey, None, value, valueEditAble, QJsonItem.ValueRole)

    def updateValue(self, value: Any) -> bool:
        itemValue: Union[QJsonItem, None] = self.value
        if itemValue is None:
            return False

        self.datas = value
        # key对应的后面的空列不允许修改
        valueEditAble = not isinstance(value, (list, tuple, dict))
        itemValue.setInfo(self, None, value, valueEditAble, QJsonItem.ValueRole)

        return True

    def toObject(self) -> Any:
        datas = self.datas
        typ = type(datas)

        if typ is dict:
            return {
                self.child(i, 0).text(): self.child(i, 1).toObject()
                for i in range(self.rowCount())
            }
        elif typ is list:
            return [self.child(i, 0).toObject() for i in range(self.rowCount())]
        elif self.value:
            return self.value.toObject()

        return self.edit


class QJsonModel(QStandardItemModel):
    def __init__(
        self,
        parent: QObject = None,
        data: dict = None,
    ) -> None:
        super().__init__(parent)
        self.setHorizontalHeaderLabels(["Key", "Value"])
        self.loadData(data)

    def loadFile(
        self, file: str, encoding: str = "utf-8", errors: str = "ignore"
    ) -> bool:
        with open(file, "rb") as f:
            return self.loadJson(f.read().decode(encoding=encoding, errors=errors))

    def loadJson(self, string: str) -> bool:
        return self.loadData(json.loads(string))

    def loadData(self, data: dict) -> bool:
        if isinstance(data, dict):
            self.__loadData(data)
            return True

        return False

    def findPath(
        self,
        path: str,
        flags=Qt.MatchFixedString
        | Qt.MatchCaseSensitive
        | Qt.MatchWrap
        | Qt.MatchRecursive,
    ):
        indexes = self.match(self.index(0, 0), QJsonItem.PathRole, path, -1, flags)
        indexes = [index for index in indexes if index.isValid()]
        return self.itemFromIndex(indexes[0]) if indexes else None

    def updateValue(self, path: str, value: Any) -> bool:
        item = self.findPath(path)
        if item is None:
            return False

        return item.updateValue(value)

    def horizontalHeaderLabels(self) -> List[str]:
        return [self.horizontalHeaderItem(i).text() for i in range(self.columnCount())]

    def clear(self):
        headers = self.horizontalHeaderLabels()
        super().clear()
        self.setHorizontalHeaderLabels(headers)

    def __loadData(self, data: Any):
        if not isinstance(data, dict):
            return

        for key, value in data.items():
            items = self.findItems(str(key))
            if items:
                itemKey: Union[QJsonItem, QStandardItem] = items[0]
                itemValue: Union[QJsonItem, None] = getattr(itemKey, "value", None)
                if itemValue is None:
                    continue
                itemKey.setText(str(key))
            else:
                itemKey = QJsonItem(str(key))
                itemValue = QJsonItem()
                self.appendRow([itemKey, itemValue])

            itemKey.setInfo(None, itemValue, value, edit=key)
            # key对应的后面的空列不允许修改
            valueEditAble = not isinstance(value, (list, tuple, dict))
            itemValue.setInfo(itemKey, None, value, valueEditAble, QJsonItem.ValueRole)

    def toDict(self) -> dict:
        item = self.invisibleRootItem()

        return {
            item.child(i).text(): item.child(i).toObject()
            for i in range(item.rowCount())
        }

    def toJson(self, ensure_ascii=True, indent=None, **kwargs) -> str:
        return json.dumps(
            self.toDict(), ensure_ascii=ensure_ascii, indent=indent, **kwargs
        )
