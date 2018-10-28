#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月29日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: OpencvWidget
@description: 
'''
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QMessageBox, QApplication
import cv2  # @UnresolvedImport
import dlib
import numpy


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

DOWNSCALE = 4


class OpencvWidget(QLabel):

    def __init__(self, *args, **kwargs):
        super(OpencvWidget, self).__init__(*args, **kwargs)
        self.fps = 24
        self.resize(800, 600)
        self.setText("请稍候，正在初始化数据和摄像头。。。")

    def start(self):
        try:
            # 检测相关
            self.detector = dlib.get_frontal_face_detector()
            self.predictor = dlib.shape_predictor(
                "data/shape_predictor_68_face_landmarks.dat")
            cascade_fn = "data/lbpcascades/lbpcascade_frontalface.xml"
            self.cascade = cv2.CascadeClassifier(cascade_fn)
            if not self.cascade:
                return QMessageBox.critical(self, "错误", cascade_fn + " 无法找到")
            self.cap = cv2.VideoCapture(0)
            if not self.cap or not self.cap.isOpened():
                return QMessageBox.critical(self, "错误", "打开摄像头失败")
            # 开启定时器定时捕获
            self.timer = QTimer(self, timeout=self.onCapture)
            self.timer.start(1000 / self.fps)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def closeEvent(self, event):
        if hasattr(self, "timer"):
            self.timer.stop()
            self.timer.deleteLater()
            self.cap.release()
            del self.predictor, self.detector, self.cascade, self.cap
        super(OpencvWidget, self).closeEvent(event)
        self.deleteLater()

    def onCapture(self):
        _, frame = self.cap.read()

        minisize = (
            int(frame.shape[1] / DOWNSCALE), int(frame.shape[0] / DOWNSCALE))
        tmpframe = cv2.resize(frame, minisize)
        tmpframe = cv2.cvtColor(tmpframe, cv2.COLOR_BGR2GRAY)  # 做灰度处理
        tmpframe = cv2.equalizeHist(tmpframe)

        # minNeighbors表示每一个目标至少要被检测到5次
        faces = self.cascade.detectMultiScale(tmpframe, minNeighbors=5)
        del tmpframe
        if len(faces) < 1:  # 没有检测到脸
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(
                frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
            del frame
            return self.setPixmap(QPixmap.fromImage(img))
        # 特征点检测描绘
        for x, y, w, h in faces:
            x, y, w, h = x * DOWNSCALE, y * DOWNSCALE, w * DOWNSCALE, h * DOWNSCALE
            # 画脸矩形
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0))
            # 截取的人脸部分
            tmpframe = frame[y:y + h, x:x + w]
            # 进行特征点描绘
            rects = self.detector(tmpframe, 1)
            if len(rects) > 0:
                landmarks = numpy.matrix(
                    [[p.x, p.y] for p in self.predictor(tmpframe, rects[0]).parts()])
                for _, point in enumerate(landmarks):
                    pos = (point[0, 0] + x, point[0, 1] + y)
                    # 在原来画面上画点
                    cv2.circle(frame, pos, 3, color=(0, 255, 0))
            # 转成Qt能显示的
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(
                frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
            del frame
            self.setPixmap(QPixmap.fromImage(img))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OpencvWidget()
    w.show()
    # 5秒后启动
    QTimer.singleShot(5000, w.start)
    sys.exit(app.exec_())
