# 列表

## [1、QListView](QListView/)

### 1. [显示自定义Widget](QListView/显示自定义Widget.py)

![截图](QListView/ScreenShot/显示自定义Widget.png)

### 2. [显示自定义Widget并排序](QListView/显示自定义Widget并排序.py)

![截图](QListView/ScreenShot/显示自定义Widget并排序.gif)

## [2、QListWidget](QListWidget/)

### 1. [自定义可拖拽Item](QListWidget/自定义可拖拽Item.py)

![截图](QListWidget/ScreenShot/自定义可拖拽Item.gif)

### 2. [腾讯视频热播列表](QListWidget/腾讯视频热播列表)
1. 使用`flowlayout`布局
2. 使用`QGridLayout`布局
3. 使用`QListWidget`，设置`self.setFlow(self.LeftToRight)`和`self.setWrapping(True)`达到横向自动排列
4. 其它知识点：
    1. 使用`QNetworkAccessManager`进行异步下载数据和图片
    2. 滚动条滑动到底部加载更多

![截图](QListWidget/腾讯视频热播列表/ScreenShot/1.gif)

### 3. [删除自定义Item](QListWidget/删除自定义Item.py)
1. 删除item时先要通过`QListWidget.indexFromItem(item).row()`得到它的行数
2. 通过`takeItem`函数取出该Item并删除掉,`item = self.listWidget.takeItem(row)`
3. 移除item对应的自定义控件`self.listWidget.removeItemWidget(item)`
4. 如果是清空所有Item，可以通过循环删除，但是删除的时候行号一直是0即可，原因和删除list数组一样。

![截图](QListWidget/ScreenShot/删除自定义Item.gif)