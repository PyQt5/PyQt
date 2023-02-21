# QListView

- 目录
  - [音乐热歌列表](#1音乐热歌列表)

## 1、音乐热歌列表
[运行 HotPlaylist.py](HotPlaylist.py)

简单思路说明：

 - 利用`QScrollArea`滚动显示，自定义的`QFlowLayout`做布局来放置自定义的Widget
 - `QNetworkAccessManager`异步下载网页和图片
 - `QScrollArea`滚动到底部触发下一页加载

自定义控件说明：

 - 主要是多个layout和控件的结合，其中图片`QLabel`为自定义，通过`setPixmap`设置图片，重写`paintEvent`绘制底部渐变矩形框和白色文字
 - 字体颜色用qss设置
 - 图标利用了`QSvgWidget`显示，可以是svg 动画（如圆形加载图）

![HotPlaylist](ScreenShot/HotPlaylist.gif)