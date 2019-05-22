# QProgressBar

- 目录
  - [常规样式美化](#1常规样式美化)
  - [圆圈进度条](#2圆圈进度条)
  - [百分比进度条](#3百分比进度条)
  - [Metro进度条](#4Metro进度条)
  - [水波纹进度条](#5水波纹进度条)

## 1、常规样式美化
[运行 SimpleStyle.py](SimpleStyle.py)

主要改变背景颜色、高度、边框、块颜色、边框、圆角

![SimpleStyle](ScreenShot/SimpleStyle.gif)

## 2、圆圈进度条
[运行 RoundProgressBar.py](RoundProgressBar.py)

![RoundProgressBar](ScreenShot/RoundProgressBar.gif)

## 3、百分比进度条
[运行 PercentProgressBar.py](PercentProgressBar.py)

![PercentProgressBar](ScreenShot/PercentProgressBar.gif)

## 4、Metro进度条
[运行 MetroCircleProgress.py](MetroCircleProgress.py)

![MetroCircleProgress](ScreenShot/MetroCircleProgress.gif)

## 5、水波纹进度条
[运行 WaterProgressBar.py](WaterProgressBar.py)

1. 利用正弦函数根据0-width的范围计算y坐标
2. 利用 `QPainterPath` 矩形或者圆形作为背景
3. 用 `QPainterPath` 把y坐标用 `lineTo` 连接起来形成一个U字形+上方波浪的闭合区间

![WaterProgressBar](ScreenShot/WaterProgressBar.gif)