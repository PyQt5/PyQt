#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2022/02/26
@author: Irony
@site: https://pyqt.site, https://github.com/PyQt5
@email: 892768447@qq.com
@file: QStyleAnimation.py
@description:
"""
from enum import IntEnum

try:
    from PyQt5.QtCore import (QAbstractAnimation, QCoreApplication, QEvent,
                              QTime)
except ImportError:
    from PySide2.QtCore import (QAbstractAnimation, QCoreApplication, QEvent,
                                QTime)

ScrollBarFadeOutDuration = 200.0
ScrollBarFadeOutDelay = 450.0

StyleAnimationUpdate = 213


class QStyleAnimation(QAbstractAnimation):

    FrameRate = IntEnum(
        'FrameRate',
        ['DefaultFps', 'SixtyFps', 'ThirtyFps', 'TwentyFps', 'FifteenFps'])

    def __init__(self, *args, **kwargs):
        super(QStyleAnimation, self).__init__(*args, **kwargs)
        self._delay = 0
        self._duration = -1
        self._startTime = QTime.currentTime()
        self._fps = self.FrameRate.ThirtyFps
        self._skip = 0

    def target(self):
        return self.parent()

    def duration(self):
        return self._duration

    def setDuration(self, duration):
        self._duration = duration

    def delay(self):
        return self._delay

    def setDelay(self, delay):
        self._delay = delay

    def startTime(self):
        return self._startTime

    def setStartTime(self, time):
        self._startTime = time

    def frameRate(self):
        return self._fps

    def setFrameRate(self, fps):
        self._fps = fps

    def updateTarget(self):
        event = QEvent(QEvent.Type(StyleAnimationUpdate))
        event.setAccepted(False)
        QCoreApplication.sendEvent(self.target(), event)
        if not event.isAccepted():
            self.stop()

    def start(self):
        self._skip = 0
        super(QStyleAnimation, self).start(QAbstractAnimation.DeleteWhenStopped)

    def isUpdateNeeded(self):
        return self.currentTime() > self._delay

    def updateCurrentTime(self, _):
        self._skip += 1
        if self._skip >= self._fps:
            self._skip = 0
            if self.parent() and self.isUpdateNeeded():
                self.updateTarget()


class QProgressStyleAnimation(QStyleAnimation):

    def __init__(self, speed, *args, **kwargs):
        super(QProgressStyleAnimation, self).__init__(*args, **kwargs)
        self._speed = speed
        self._step = -1

    def animationStep(self):
        return self.currentTime() / (1000.0 / self._speed)

    def progressStep(self, width):
        step = self.animationStep()
        progress = (step * width / self._speed) % width
        if (((step * width / self._speed) % (2 * width)) >= width):
            progress = width - progress
        return progress

    def speed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def isUpdateNeeded(self):
        if super(QProgressStyleAnimation, self).isUpdateNeeded():
            current = self.animationStep()
            if self._step == -1 or self._step != current:
                self._step = current
                return True
        return False
