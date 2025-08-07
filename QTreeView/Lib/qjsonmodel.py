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
from functools import reduce
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
        self.keyItem = key
        self.valueItem = value
        self.edit = edit
        self.datas = datas

    @property
    def keyItem(self) -> Union["QJsonItem", None]:
        # 上一级key item
        item = self.data(self.KeyRole)
        if not isinstance(item, QJsonItem):
            return None
        return item

    @keyItem.setter
    def keyItem(self, value: "QJsonItem") -> None:
        self.setData(value, self.KeyRole)

    @property
    def valueItem(self) -> "QJsonItem":
        # 当前value item
        return self.data(self.ValueRole)

    @valueItem.setter
    def valueItem(self, value: "QJsonItem") -> None:
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
        self.setData(value, self.DatasRole)
        if self._role == QJsonItem.ValueRole:
            if not isinstance(value, (list, tuple, dict)):
                self.edit = value
            return
        self.__loadData(value)

    @property
    def type(self) -> Any:
        return type(self.edit)

    @property
    def role(self) -> int:
        return self._role

    @property
    def path(self) -> str:
        item = self.keyItem if self._role == self.ValueRole else self
        paths = []

        while item:
            paths.append(item.text())
            item = item.keyItem

        paths.reverse()
        return QJsonItem.Sep.join(paths)

    def data(self, role: int = Qt.DisplayRole) -> Any:
        if role == self.PathRole:
            return self.path

        return super().data(role)

    def setData(self, data: Any, role: int = Qt.EditRole):
        super().setData(data, role)

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
        itemValue: Union[QJsonItem, None] = self.valueItem
        if itemValue is None:
            return False
        if itemValue.datas == value:
            return True

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
        elif self.valueItem:
            return self.valueItem.toObject()

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

    def loadData(self, data: dict, force: bool = False) -> bool:
        if isinstance(data, dict):
            if force:
                self.clear()
            self.__loadData(data)
            return True

        return False

    def horizontalHeaderLabels(self) -> List[str]:
        return [self.horizontalHeaderItem(i).text() for i in range(self.columnCount())]

    def clear(self):
        headers = self.horizontalHeaderLabels()
        super().clear()
        self.setHorizontalHeaderLabels(headers)

    def findPath(
        self,
        path: str,
        flags=Qt.MatchFixedString
        | Qt.MatchCaseSensitive
        | Qt.MatchWrap
        | Qt.MatchRecursive,
    ) -> Union[QJsonItem, None]:
        indexes = self.match(self.index(0, 0), QJsonItem.PathRole, path, -1, flags)
        indexes = [index for index in indexes if index.isValid()]
        return self.itemFromIndex(indexes[0]) if indexes else None  # type: ignore

    def updateValue(
        self, path: str, value: Any, item: Union[QJsonItem, None] = None
    ) -> bool:
        item = item or self.findPath(path)
        if item is None:
            keys = path.split(QJsonItem.Sep)
            self.__loadData(reduce(lambda val, key: {key: val}, reversed(keys), value))
            return True

        return item.updateValue(value)

    def __findItem(
        self, key: str, parent=None
    ) -> Union[QStandardItem, "QJsonItem", None]:
        parent = parent or self.invisibleRootItem()
        for row in range(parent.rowCount()):
            item = parent.child(row)
            if item.text() == key:
                return item

        return None

    def __createItem(self, key: str, value: Any, parent=None):
        parent = parent or self.invisibleRootItem()

        itemKey = QJsonItem(str(key))
        itemValue = QJsonItem()
        parent.appendRow([itemKey, itemValue])

        itemKey.setInfo(parent, itemValue, value, edit=key)
        # key对应的后面的空列不允许修改
        valueEditAble = not isinstance(value, (list, tuple, dict))
        itemValue.setInfo(itemKey, None, value, valueEditAble, QJsonItem.ValueRole)

    def __loadData(self, data: Any, parent=None):
        if not isinstance(data, dict):  # 更新值
            itemKey = parent
            if itemKey:
                itemKey.updateValue(data)
            return

        parent = parent or self.invisibleRootItem()

        for key, value in data.items():
            key = str(key)
            itemKey = self.__findItem(key, parent)
            if not itemKey:
                self.__createItem(key, value, parent)
            else:
                self.__loadData(value, itemKey)

    def toDict(self) -> dict:
        item = self.invisibleRootItem()

        return {
            item.child(i).text(): item.child(i).toObject()
            for i in range(item.rowCount())
        }

    def toJson(self, ensure_ascii=False, indent=None, **kwargs) -> str:
        return json.dumps(
            self.toDict(), ensure_ascii=ensure_ascii, indent=indent, **kwargs
        )
