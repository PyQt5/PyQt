#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月18日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: 堆叠柱状图
@description: 
'''
import sys

from PyQt5.QtChart import QChartView, QChart
from PyQt5.QtWidgets import QApplication


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class StackBarChart(QChartView):

    def __init__(self, *args, **kwargs):
        super(StackBarChart, self).__init__(*args, **kwargs)
        self._chart = QChart()
        self.setChart(self._chart)

    def initUi(self, file):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = StackBarChart()
    w.show()
    sys.exit(app.exec_())
