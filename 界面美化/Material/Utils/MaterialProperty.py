#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年2月3日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: MaterialProperty
@description: 
'''
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QColor, QFont

from Material.Utils.Colors import _Color, Colors  # @UnresolvedImport


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

class MaterialProperty(QObject):

    def _getColor(self, color: [str, int, tuple, list]) -> QColor:
        '''
        :param color: str, int, tuple, list
        '''
        if isinstance(color, _Color) or isinstance(color, QColor):
            return color
        elif isinstance(color, tuple) or isinstance(color, list):
            for c in color:
                if not isinstance(c, int):
                    return _Color(255, 255, 255)
            if len(color) == 3 or len(color) == 4:
                return _Color(*color)
        elif isinstance(color, int):
            return _Color(color)
        elif isinstance(color, str) and color.startswith("#"):
            return _Color(color)
        else:
            return _Color(255, 255, 255)

    @property
    def title(self) -> str:
        '''get title(标题)'''
        if not hasattr(self, "_title"):
            self._title = ""
        return self._title

    @title.setter
    def title(self, title: str):
        '''
        set title(设置标题)
        :param title: str
        '''
        self._title = title if isinstance(title, str) else ""
        self.setTitle(title)

    def setTitle(self, title):
        pass

    @property
    def content(self) -> str:
        '''get content(内容)'''
        if not hasattr(self, "_content"):
            self._content = ""
        return self._content

    @content.setter
    def content(self, content: str):
        '''
        set content(设置内容)
        :param content: str
        '''
        self._content = content if isinstance(content, str) else ""
        self.setContent(content)

    def setContent(self, content):
        pass

    @property
    def fontName(self) -> str:
        '''get font name(字体)'''
        if not hasattr(self, "_fontName"):
            self._fontName = QFont().defaultFamily()
        return self._fontName

    @fontName.setter
    def fontName(self, name: str):
        '''
        set font name(设置字体)
        :param name: str
        '''
        self._fontName = name if isinstance(
            name, str) else QFont().defaultFamily()

    @property
    def fontSize(self) -> int:
        '''get font size(字体大小)'''
        if not hasattr(self, "_fontSize"):
            self._fontSize = 16  # 24
        return self._fontSize

    @fontSize.setter
    def fontSize(self, size: int):
        '''
        set font size(设置字体大小)
        :param size: int
        '''
        self._fontSize = size if isinstance(size, int) else 16  # 24

    @property
    def titleFontSize(self) -> int:
        '''get font size(字体大小)'''
        if not hasattr(self, "_titleFontSize"):
            self._titleFontSize = 14
        return self._titleFontSize

    @titleFontSize.setter
    def titleFontSize(self, size: int):
        '''
        set title font size(设置字体大小)
        :param size: int
        '''
        self._titleFontSize = size if isinstance(size, int) else 14

    @property
    def radioSize(self) -> int:
        '''get radio circle size(RadioButton左侧圆形大小)'''
        if not hasattr(self, "_radioSize"):
            self._radioSize = 16
        return self._radioSize

    @radioSize.setter
    def radioSize(self, size: int):
        '''
        set radio circle size(设置RadioButton左侧圆形大小)
        :param size: int
        '''
        self._radioSize = size if isinstance(size, int) and size >= 16 else 16

    @property
    def borderWidth(self) -> int:
        '''return top bottom left right border width(上下左右边框的宽度)'''
        if not hasattr(self, "_borderWidth"):
            self._borderWidth = 2
        return self._borderWidth

    @borderWidth.setter
    def borderWidth(self, width: int):
        '''
        set top bottom left right border width(设置上下左右边框的宽度)
        :param width: 2
        '''
        try:
            self._borderWidth = int(width)
        except:
            self._borderWidth = 2

    @property
    def borderRadius(self) -> int:
        '''return top bottom left right rounded corner(上下左右圆角大小)'''
        if not hasattr(self, "_borderRadius"):
            self._borderRadius = 2
        return self._borderRadius

    @borderRadius.setter
    def borderRadius(self, radius: int):
        '''
        set top bottom left right rounded corner(设置上下左右圆角大小)
        :param radius: 2
        '''
        try:
            self._borderRadius = int(radius)
        except:
            self._borderRadius = 2

    @property
    def borderColor(self) -> QColor:
        '''the border color, default is transparent(边框颜色,默认透明)'''
        if not hasattr(self, "_borderColor"):
            self._borderColor = Colors.TRANSPARENT.default    # 透明
        return self._borderColor

    @borderColor.setter
    def borderColor(self, color: [str, int, tuple, list]):
        '''set border color(设置边框颜色)
        :param color: str, int, tuple, list
        Example:
            xx.borderColor = (255, 255, 255) # white(白色)
            xx.borderColor = [255, 255, 255, 100] # white color with alpha = 100(白色带100透明)
            xx.borderColor = 55 # RGBA: (0, 0, 55, 255)
            xx.borderColor = "#FFFFFF" # RGBA: (255, 255, 255, 255)
        '''
        self._borderColor = self._getColor(color)

    @property
    def borderColorDisable(self) -> QColor:
        '''get disable border color(获取禁用状态下的边框颜色)'''
        if not hasattr(self, "_borderColorDisable"):
            # default color is black with 0.6 alpha(0.6透明度灰色)
            self._borderColorDisable = Colors.GREY.default
        return self._borderColorDisable

    @borderColorDisable.setter
    def borderColorDisable(self, color: [str, int, tuple, list]):
        '''
        set disable border color(设置禁用状态边框颜色)
        :param color: str, int, tuple, list
        Example:
            xx.borderColorDisable = (255, 255, 255) # white(白色)
            xx.borderColorDisable = [255, 255, 255, 100] # white color with alpha = 100(白色带100透明)
            xx.borderColorDisable = 55 # RGBA: (0, 0, 55, 255)
            xx.borderColorDisable = "#FFFFFF" # RGBA: (255, 255, 255, 255)
        '''
        self._borderColorDisable = self._getColor(color)

    @property
    def lineHintColor(self) -> QColor:
        '''get lineedit hint line color(获取输入框底部横线颜色)'''
        if not hasattr(self, "_lineHintColor"):
            # default grey 300(灰色 300)
            self._lineHintColor = Colors.GREY.C300
        return self._lineHintColor

    @lineHintColor.setter
    def lineHintColor(self, color: [str, int, tuple, list]):
        '''
        set lineedit hint line color(设置输入框底部横线颜色)
        :param color: str, int, tuple, list
        Example:
            xx._lineHintColor = (255, 255, 255) # white(白色)
            xx._lineHintColor = [255, 255, 255, 100] # white color with alpha = 100(白色带100透明)
            xx._lineHintColor = 55 # RGBA: (0, 0, 55, 255)
            xx._lineHintColor = "#FFFFFF" # RGBA: (255, 255, 255, 255)
        '''
        self._lineHintColor = self._getColor(color)

    @property
    def lineColor(self) -> QColor:
        '''get lineedit line color(获取输入框底部横线动画颜色)'''
        if not hasattr(self, "_lineColor"):
            self._lineColor = Colors.BLUE.default    # default blue(蓝色)
        return self._lineColor

    @lineColor.setter
    def lineColor(self, color: [str, int, tuple, list]):
        '''
        set lineedit line color(设置输入框底部横线颜色)
        :param color: str, int, tuple, list
        Example:
            xx._lineColor = (255, 255, 255) # white(白色)
            xx._lineColor = [255, 255, 255, 100] # white color with alpha = 100(白色带100透明)
            xx._lineColor = 55 # RGBA: (0, 0, 55, 255)
            xx._lineColor = "#FFFFFF" # RGBA: (255, 255, 255, 255)
        '''
        self._lineColor = self._getColor(color)

    @property
    def fontColor(self) -> QColor:
        '''get font color(获取当前字体颜色)'''
        if not hasattr(self, "_fontColor"):
            self._fontColor = Colors.BLACK.default    # default black(默认黑色)
        return self._fontColor

    @fontColor.setter
    def fontColor(self, color: [str, int, tuple, list]):
        '''
        set font color(设置字体颜色)
        :param color: str, int, tuple, list
        Example:
            xx.fontColor = (255, 255, 255) # white(白色)
            xx.fontColor = [255, 255, 255, 100] # white color with alpha = 100(白色带100透明)
            xx.fontColor = 55 # RGBA: (0, 0, 55, 255)
            xx.fontColor = "#FFFFFF" # RGBA: (255, 255, 255, 255)
        '''
        self._fontColor = self._getColor(color)

    @property
    def fontColorDisable(self) -> QColor:
        '''get disable font color(获取禁用状态下的字体颜色)'''
        if not hasattr(self, "_fontColorDisable"):
            # default color is black with 0.6 alpha(0.6透明度灰色)
            self._fontColorDisable = Colors.GREY.default
        return self._fontColorDisable

    @fontColorDisable.setter
    def fontColorDisable(self, color: [str, int, tuple, list]):
        '''
        set disable font color(设置禁用状态字体颜色)
        :param color: str, int, tuple, list
        Example:
            xx.fontColorDisable = (255, 255, 255) # white(白色)
            xx.fontColorDisable = [255, 255, 255, 100] # white color with alpha = 100(白色带100透明)
            xx.fontColorDisable = 55 # RGBA: (0, 0, 55, 255)
            xx.fontColorDisable = "#FFFFFF" # RGBA: (255, 255, 255, 255)
        '''
        self._fontColorDisable = self._getColor(color)

    @property
    def backgroundColor(self):
        '''get default background color(获取当前背景颜色)'''
        if not hasattr(self, "_backgroundColor"):
            self._backgroundColor = Colors.WHITE.default    # 白色
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color: [str, int, tuple, list]):
        '''
        set background color(设置背景颜色)
        :param color: str, int, tuple, list
        Example:
            xx.backgroundColor = (255, 255, 255) # white
            xx.backgroundColor = [255, 255, 255, 100] # white color with alpha = 100
            xx.backgroundColor = 55 # RGBA: (0, 0, 55, 255)
            xx.backgroundColor = "#FFFFFF" # RGBA: (255, 255, 255, 255)
        '''
        self._backgroundColor = self._getColor(color)

    @property
    def backgroundColorDisable(self):
        '''get disable background color(获取禁用状态下的背景颜色)'''
        if not hasattr(self, "_backgroundColorDisable"):
            # 0.6透明度背景颜色
            self._backgroundColorDisable = self.backgroundColor.getOpacity(0.5)
        return self._backgroundColorDisable

    @backgroundColorDisable.setter
    def backgroundColorDisable(self, color: [str, int, tuple, list]):
        '''
        set disable background color(设置禁用状态背景颜色)
        :param color: str, int, tuple, list
        Example:
            xx.backgroundColorDisable = (255, 255, 255) # white
            xx.backgroundColorDisable = [255, 255, 255, 100] # white color with alpha = 100
            xx.backgroundColorDisable = 55 # RGBA: (0, 0, 55, 255)
            xx.backgroundColorDisable = "#FFFFFF" # RGBA: (255, 255, 255, 255)
        '''
        self._backgroundColorDisable = self._getColor(color)

    @property
    def rippleColor(self):
        '''get rippleEffect color(获取波纹颜色)'''
        if not hasattr(self, "_rippleColor"):
            # 0.2透明度背景颜色
            self._rippleColor = Colors.WHITE.default.getOpacity(0.5)
        return self._rippleColor

    @rippleColor.setter
    def rippleColor(self, color: [str, int, tuple, list]):
        '''
        set rippleEffect(设置波纹颜色)
        :param color: str, int, tuple, list
        Example:
            xx.rippleColor = (255, 255, 255) # white
            xx.rippleColor = [255, 255, 255, 100] # white color with alpha = 100
            xx.rippleColor = 55 # RGBA: (0, 0, 55, 255)
            xx.rippleColor = "#FFFFFF" # RGBA: (255, 255, 255, 255)
        '''
        self._rippleColor = self._getColor(color)

if __name__ == "__main__":
    help(MaterialProperty)
