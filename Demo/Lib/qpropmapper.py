#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2025/08/05
@file: qpropertymapper.py
@description:
"""

from typing import Any, Union

from box import Box

try:
    from PyQt5.QtCore import (
        QDateTime,
        QMetaProperty,
        QObject,
        Qt,
    )
    from PyQt5.QtCore import (
        pyqtSignal as Signal,
    )
    from PyQt5.QtWidgets import QWidget
except ImportError:
    from PySide2.QtCore import (
        QDateTime,
        QMetaProperty,
        QObject,
        Qt,
        Signal,
    )
    from PySide2.QtWidgets import QWidget


class DictBox(Box):
    def keys(self, dotted: bool = False):
        if not dotted:
            return super().keys()

        if not self._box_config["box_dots"]:
            raise Exception(
                "Cannot return dotted keys as this Box does not have `box_dots` enabled"
            )

        keys = set()
        for key, value in self.items():
            added = False
            if isinstance(key, str):
                if isinstance(value, Box):
                    for sub_key in value.keys(dotted=True):
                        keys.add(f"{key}.{sub_key}")
                        added = True
                if not added:
                    keys.add(key)
        return sorted(keys, key=lambda x: str(x))


class QPropertyMapper(QObject):
    Verbose = False
    propertyChanged = Signal(int, str, object)
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
        data = kwargs.pop("data", {})
        super().__init__(*args, **kwargs)
        self._widgetKey = {}
        self._keyWidget = {}
        self.propertyChanged.connect(self.onPropertyChanged)
        self.loadData(data, clear=False)

    def __enter__(self):
        self.__log("[__enter__]: block signals")
        self.blockSignals(True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__log("[__exit__]: unblock signals")
        self.blockSignals(False)

    def event(self, ev) -> bool:
        if ev.type() == ev.DynamicPropertyChange:
            name = bytes(ev.propertyName()).decode()
            value = self.property(name)
            self.propertyChanged.emit(value is not None, name, value)
        return super().event(ev)

    def clear(self):
        self.__log("[clear]: clear datas")
        with self:
            keys = self.dynamicPropertyNames().copy()
            for key in keys:
                self.setProperty(bytes(key).decode(), None)
            # clear binds

    def loadData(self, data: dict, clear: bool = False):
        self.__log("[loadData]: load data")
        if clear:
            self.clear()
        data = DictBox(data, default_box=True, box_dots=True)
        for key, value in data.items(True):
            self.setProperty(str(key), value)

    def toDict(self, raw=True) -> dict:
        data = DictBox(default_box=True, box_dots=True)
        for key in self.dynamicPropertyNames():
            key = bytes(key).decode()
            try:
                data[key] = self.property(key)
            except Exception as e:
                self.__log(f"[toDict]: {e}")
        if raw:
            return data.to_dict()
        return data

    def toJson(self, indent=None, **kwargs) -> str:
        return self.toDict(False).to_json(indent=indent, **kwargs)

    def getProperty(
        self, widget: QWidget, prop: str = ""
    ) -> Union[QMetaProperty, None]:
        """获取控件的对应属性

        Args:
            widget (QWidget): 控件对象
            prop (str, optional): 指定的属性. 默认为 ""

        Returns:
            Union[QMetaProperty, None]: 返回属性对象
        """
        qmo = widget.metaObject()
        props = [prop] if prop else self.Props

        for prop in props:
            idx = qmo.indexOfProperty(prop)
            if idx > -1:
                p = qmo.property(idx)
                if p.isReadable() and p.isWritable():
                    self.__log(
                        f"[getProperty]: get prop: {prop} of widget: {self.__widgetInfo(widget)}"
                    )
                    return p

        return None

    def bind(self, widget: QWidget, key: str, default: Any = None, prop: str = ""):
        # 1. 记录widget和key
        if widget not in self._widgetKey:
            self.__log(
                f"[bind]: bind key: {key} to widget: {self.__widgetInfo(widget)}"
            )
            self._widgetKey[widget] = {
                "key": key,
                "prop": self.getProperty(widget, prop),
            }
            # 2. 设置控件的默认值
            with self:
                self.__setValue(widget, key, default)

        # 3. 记录所有关联的widget
        if key not in self._keyWidget:
            self._keyWidget[key] = set()
        self._keyWidget[key].add(widget)

        # 4. 绑定widget的相关信号
        for signal in self.Signal:
            signal = getattr(widget, signal, None)
            if signal:
                self.__log(
                    f"[bind]: connect key: {key}, signal: {signal} of widget: {self.__widgetInfo(widget)}"
                )
                signal.connect(self.__setData)
                break

    def __log(self, *args):
        if self.Verbose:
            print(*args)

    def __widgetInfo(self, widget: QWidget) -> Union[str, None]:
        try:
            return f"<{widget.__class__.__name__}(name={widget.objectName()}) {hex(id(widget))}>"
        except Exception:
            return None

    def __getDefault(self, widget: QWidget, default: Any = None):
        """获取控件的默认值

        Args:
            widget (QWidget): 控件对象
            default (Any, optional): 默认值. 默认为None

        Returns:
            Any: 默认值
        """
        if default:
            return default

        # 1. 从记录表中获取窗口的属性对象
        prop: Union[QMetaProperty, None] = self._widgetKey[widget]["prop"]
        if prop is None:
            return None

        # 2. 获取属性值并进行一些转换
        value = prop.read(widget)
        if value is not None:
            if prop.name() == "dateTime":
                return value.toString("yyyy-MM-dd HH:mm:ss")
            elif prop.name() == "html" and len(widget.property("plainText")) == 0:
                return ""
            return value

        return None

    def __setValue(
        self,
        widget: QWidget,
        key: str,
        default: Any = None,
        updated: bool = False,
    ):
        value: Any = default

        # 1. 首次同步widget属性值到mapper
        if not updated:
            value = self.__getDefault(widget, default)
            self.__log(
                f"[__setValue]: setProperty key: {key}, value: {value} of widget: {self.__widgetInfo(widget)}"
            )
            self.setProperty(key, value)

        if value is None:
            return

        # 2. 设置widget的属性值
        prop: Union[QMetaProperty, None] = self._widgetKey[widget]["prop"]
        if prop is not None:
            if prop.name() == "dateTime" and isinstance(value, str):
                value = QDateTime.fromString(value, Qt.ISODate)
            self.__log(
                f"[__setValue]: update key: {key}, value: {value} of widget: {self.__widgetInfo(widget)}"
            )
            prop.write(widget, value)

    def __setData(self, *args, **kwargs):
        """控件值发生变化时，更新关联控件以及设置mapper数据"""

        # 1. 获取发送者widget关联的key和prop
        sender = self.sender()
        info = self._widgetKey.get(sender, {})
        key = info.get("key", None)
        prop: Union[QMetaProperty, None] = info.get("prop", None)
        if key is None or prop is None:
            self.__log(
                f"[__setData]: sender {self.__widgetInfo(sender)} has no key or prop"
            )
            return

        # 2. 读取发送者widget的属性值
        value = prop.read(sender)
        if value is not None:
            if prop.name() == "dateTime":
                value = value.toString("yyyy-MM-dd HH:mm:ss")
            elif prop.name() == "html" and len(sender.property("plainText")) == 0:
                value = ""

        if value is None:
            return

        # 更新关联的key
        self.__log(
            f"[__setData]: update key: {key}, value: {value} from widget: {self.__widgetInfo(sender)}"
        )
        self.setProperty(key, value)

    def onPropertyChanged(self, op: int, key: str, value: Any):
        """mapper属性值发生变化时，更新关联的widget

        Args:
            op (int): 操作类型（1=添加，0=删除）
            key (str): 属性名字
            value (Any): 属性值
        """
        if op != 1:
            return

        # 1. 获取mapper中key对应的值
        value = self.property(key)
        if value is None:
            return

        # 更新关联的widget
        for widget in self._keyWidget.get(key, []):
            self.__log(
                f"[onPropertyChanged]: set key: {key}, value: {value} of widget: {self.__widgetInfo(widget)}"
            )
            try:
                self.__setValue(widget, key, value, updated=True)
            except Exception as e:
                self.__log(f"[onPropertyChanged]: __setValue failed: {e}")
