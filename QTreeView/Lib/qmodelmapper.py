#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2025/08/08
@file: qmodelmapper.py
@description:
"""

from copy import deepcopy
from typing import Any, List, Union

from Lib.qjsonmodel import QJsonModel

try:
    from PyQt5.QtCore import (
        QDateTime,
        QMetaProperty,
        QModelIndex,
        QObject,
        Qt,
        QTimer,
    )
    from PyQt5.QtCore import pyqtSignal as Signal
    from PyQt5.QtWidgets import QWidget
except ImportError:
    from PySide2.QtCore import (
        QDateTime,
        QMetaProperty,
        QModelIndex,
        QObject,
        Qt,
        QTimer,
        Signal,
    )
    from PySide2.QtWidgets import QWidget


class QModelMapper(QObject):
    Debug = False
    valueChanged = Signal()
    Signal = (
        "dateTimeChanged",
        "currentTextChanged",
        "valueChanged",
        "toggled",
        "textChanged",
    )
    Props = (
        "dateTime",
        "html",
        "plainText",
        "currentText",
        "checked",
        "value",
        "text",
    )

    def __init__(self, *args, **kwargs):
        self._delay = kwargs.pop("delay", 50)
        data = kwargs.pop("data", {})
        super().__init__(*args, **kwargs)
        self._old = deepcopy(data)
        self._widgetkey = {}
        self._keywidget = {}
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.valueChanged.emit)
        self._model = QJsonModel(self.parent(), data=data)
        self._model.dataChanged.connect(self.onItemDataChanged)

    def bind(self, widget: QWidget, key: str, default: Any = None, prop: str = ""):
        if widget not in self._widgetkey:
            self._widgetkey[widget] = {
                "key": key,
                "prop": self.getProperty(widget, prop),
            }
            self._setValue(widget, key, default)

        # record all widgets for key
        if key not in self._keywidget:
            self._keywidget[key] = set()
        self._keywidget[key].add(widget)

        for signal in self.Signal:
            signal = getattr(widget, signal, None)
            if signal:
                signal.connect(self._setData)
                break

    def isModify(self) -> bool:
        return self._model.toDict() != self._old

    def getModel(self) -> QJsonModel:
        return self._model

    def getData(self) -> dict:
        return self._model.toDict()

    def getJson(self, ensure_ascii=False, indent=None, **kwargs) -> str:
        return self._model.toJson(ensure_ascii=ensure_ascii, indent=indent, **kwargs)

    def setData(self, data: dict, force: bool = False):
        if force:
            self._old = deepcopy(data)
        else:
            self._old.update(data)

        if force:
            self._model.blockSignals(True)
        self._model.loadData(data, force)
        if force:
            self._model.blockSignals(False)

    def getProperty(
        self, widget: QWidget, prop: str = ""
    ) -> Union[QMetaProperty, None]:
        qmo = widget.metaObject()
        props = [prop] if prop else self.Props
        widgetProps = (
            qmo.property(i)
            for i in range(
                QWidget.staticMetaObject.propertyCount(), qmo.propertyCount()
            )
        )
        widgetProps = [
            p for p in widgetProps if p and p.isReadable() and p.isWritable()
        ]

        rets = [p for prop in props for p in widgetProps if p.name() == prop]
        return rets[0] if rets else None

    def _getDefault(self, widget: QWidget, default: Any = None):
        if default:
            return default

        prop: Union[QMetaProperty, None] = self._widgetkey[widget]["prop"]
        if prop is None:
            return None

        value = prop.read(widget)
        if value is not None:
            if prop.name() == "dateTime":
                return value.toString("yyyy-MM-dd HH:mm:ss")
            elif prop.name() == "html" and len(widget.property("plainText")) == 0:
                return ""
            return value

        return None

    def _setValue(
        self,
        widget: QWidget,
        key: str,
        default: Any = None,
        updated: bool = False,
        block=False,
    ):
        created = False
        value: Any = default

        if not updated:
            item = self._model.findPath(key)
            if item is None:
                value = self._getDefault(widget, default)
                created = self._model.updateValue(key, value, item)
            else:
                # value from model
                if item.valueItem:
                    value = item.valueItem.edit
                    created = default != value
                block = True
            if value is None:
                return

        if block:
            widget.blockSignals(True)

        prop: Union[QMetaProperty, None] = self._widgetkey[widget]["prop"]
        if prop is not None:
            if prop.name() == "dateTime" and isinstance(value, str):
                value = QDateTime.fromString(value, Qt.ISODate)
            prop.write(widget, value)
            if created:
                self._timer.start(self._delay)

        if block:
            widget.blockSignals(False)

    def _setData(self, *args, **kwargs):
        sender = self.sender()
        info = self._widgetkey.get(sender, {})
        key = info.get("key", None)
        prop: Union[QMetaProperty, None] = info.get("prop", None)
        if key is None or prop is None:
            return

        value = prop.read(sender)
        if value is not None:
            if prop.name() == "dateTime":
                value = value.toString("yyyy-MM-dd HH:mm:ss")
            elif prop.name() == "html" and len(sender.property("plainText")) == 0:
                value = ""

        if value is None:
            return

        self._timer.start(self._delay)

        # 更新关联的widget
        for widget in self._keywidget.get(key, []):
            if widget != sender:
                if self.Debug:
                    print(f"view to view({widget}) = {value}")
                self._setValue(widget, key, value, updated=True, block=True)

        # 更新关联的model
        if self.Debug:
            print(f"view({sender}) to model = {value}")
        if not self._model.updateValue(key, value):
            return

    def onItemDataChanged(
        self, topLeft: QModelIndex, bottomRight: QModelIndex, roles: List[int]
    ):
        item = self._model.itemFromIndex(topLeft)
        if not item or Qt.EditRole not in roles or item.valueItem:
            return

        path = getattr(item, "path", None)
        if not path:
            return

        # 更新关联的widget
        value = item.edit
        for widget in self._keywidget.get(path, []):
            if self.Debug:
                print(f"model to view({widget}) = {value}")
            self._setValue(widget, path, value, updated=True, block=True)
