#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月18日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, http://coding.net/u/892768447, http://github.com/892768447
@email: 892768447@qq.com
@file: ChartHelper
@description: 
'''
import json

from PyQt5.QtChart import QChart
import chardet


__version__ = "0.0.1"


class OptionAnalysis:

    def __init__(self, chart, file):
        self._chart = chart
        with open(file, "rb") as fp:
            data = fp.read()
            encoding = chardet.detect(data) or {}
            data = data.decode(encoding.get("encoding") or "utf-8")
        self.__analysis(json.loads(data))

    def __getAnimation(self, value):
        '''
        get animation type
        :param value: all|grid|series|no
        :rtype: QChart.AnimationOption
        '''
        if value == "all":
            return QChart.AllAnimations
        elif value == "grid":
            return QChart.GridAxisAnimations
        elif value == "series":
            return QChart.SeriesAnimations
        else:
            return QChart.NoAnimation

    def __analysis(self, datas):
        '''
        analysis json data
        :param datas: json data
        '''
        pass
