#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月25日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QtNinePatch
@description: 
"""
from math import floor

try:
    from PyQt5.QtCore import Qt, QRect
    from PyQt5.QtGui import qAlpha, QPixmap, QPainter
except ImportError:
    from PySide2.QtCore import Qt, QRect
    from PySide2.QtGui import qAlpha, QPixmap, QPainter


class Part:

    def __init__(self, pos=0, length=0, stretchable=False):
        self.pos = pos
        self.length = length
        self.stretchable = stretchable


def isStretchableMarker(pixel):
    return (qAlpha(pixel) >> 7) & 1


def resize9patch(image, dw, dh):
    sw = image.width()
    sh = image.height()
    if sw > 2 and sh > 2 and dw > 0 and dh > 0:
        pixmap = QPixmap(dw, dh)
        pixmap.fill(Qt.transparent)
        pr = QPainter(pixmap)
        pr.setRenderHint(QPainter.Antialiasing)
        pr.setRenderHint(QPainter.SmoothPixmapTransform)

        horz = []
        vert = []
        horz_stretch = 0
        vert_stretch = 0

        pos = 0
        last = image.pixel(1, 0)
        for x in range(1, sw - 1):
            nextP = image.pixel(x + 1, 0)
            if isStretchableMarker(last) != isStretchableMarker(nextP) or x == sw - 2:
                stretchable = isStretchableMarker(last)
                length = x - pos
                horz.append(Part(pos, length, stretchable))
                if stretchable:
                    horz_stretch += length
                last = nextP
                pos = x
        pos = 0
        last = image.pixel(0, 1)
        for y in range(1, sh - 1):
            nextP = image.pixel(0, y + 1)
            if isStretchableMarker(last) != isStretchableMarker(nextP) or y == sh - 2:
                stretchable = isStretchableMarker(last)
                length = y - pos
                vert.append(Part(pos, length, stretchable))
                if stretchable:
                    vert_stretch += length
                last = nextP
                pos = y

        horz_mul = 0
        vert_mul = 0
        if horz_stretch > 0:
            horz_mul = float((dw - (sw - 2 - horz_stretch)) / horz_stretch)
        if vert_stretch > 0:
            vert_mul = float((dh - (sh - 2 - vert_stretch)) / vert_stretch)
        dy0 = 0
        dy1 = 0
        vstretch = 0
        len_vert = len(vert)
        len_horz = len(horz)
        for i in range(len_vert):
            sy0 = vert[i].pos
            sy1 = vert[i].pos + vert[i].length
            if i + 1 == len_vert:
                dy1 = dh
            elif vert[i].stretchable:
                vstretch += float(vert[i].length * vert_mul)
                s = floor(vstretch)
                vstretch -= s
                dy1 += int(s)
            else:
                dy1 += vert[i].length
            dx0 = 0
            dx1 = 0
            hstretch = 0
            for j in range(len_horz):
                sx0 = horz[j].pos
                sx1 = horz[j].pos + horz[j].length
                if j + 1 == len_horz:
                    dx1 = dw
                elif horz[j].stretchable:
                    hstretch += float(horz[j].length * horz_mul)
                    s = floor(hstretch)
                    hstretch -= s
                    dx1 += int(s)
                else:
                    dx1 += horz[j].length
                pr.drawImage(QRect(dx0, dy0, dx1 - dx0, dy1 - dy0),
                             image, QRect(sx0 + 1, sy0 + 1, sx1 - sx0, sy1 - sy0))
                dx0 = dx1
            dy0 = dy1
        return pixmap
    return QPixmap()


def createPixmapFromNinePatchImage(image, dw, dh):
    w = dw
    h = dh
    if w < image.width() or h < image.height():  # shrink
        w = max(image.width(), w)
        h = max(image.height(), h)
        pm1 = resize9patch(image, w, h)
        if pm1.isNull():
            return QPixmap()
        pm2 = QPixmap(dw, dh)
        pm2.fill(Qt.transparent)
        pr = QPainter(pm2)
        pr.setRenderHint(QPainter.Antialiasing)
        pr.setRenderHint(QPainter.SmoothPixmapTransform)
        pr.drawPixmap(0, 0, dw, dh, pm1, 0, 0, w, h)
        return pm2
    else:
        return resize9patch(image, dw, dh)
