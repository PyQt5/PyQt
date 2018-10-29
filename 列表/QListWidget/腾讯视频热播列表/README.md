# 腾讯视频热播列表

简单思路说明：

 - 利用QScrollArea滚动显示，QGridLayout或者FlowLayout做布局来放置自定义的Widget
 - QNetworkAccessManager异步下载网页和图片
 - QScrollArea滚动到底部触发下一页加载

自定义控件说明：

 - 主要是多个layout和控件的结合，其中图片QLabel为自定义，通过setPixmap设置图片，重写paintEvent绘制底部渐变矩形框和白色文字
 - 字体颜色用qss设置
 - 图标利用了QSvgWidget显示，可以是svg 动画（如圆形加载图）


# 截图

使用QGridLayout 固定列数效果图

![截图1](ScreenShot/1.gif)

使用自定义布局FlowLayout 自动列数效果图
![截图2](ScreenShot/2.gif)

使用QListWidget 配合setFlow(QListWidget.LeftToRight)和
setWrapping(True)和
setResizeMode(QListWidget.Adjust)达到类似FlowLayout的效果

![截图3](ScreenShot/3.gif)