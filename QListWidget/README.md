# QListView

## 1、删除自定义Item
[运行](DeleteCustomItem.py)

1. 删除item时先要通过`QListWidget.indexFromItem(item).row()`得到它的行数
2. 通过`takeItem`函数取出该Item并删除掉,`item = self.listWidget.takeItem(row)`
3. 移除item对应的自定义控件`self.listWidget.removeItemWidget(item)`
4. 如果是清空所有Item，可以通过循环删除，但是删除的时候行号一直是0即可，原因和删除list数组一样。

![CustomWidgetItem](ScreenShot/DeleteCustomItem.gif)

## 2、自定义可拖拽Item
[运行](DragDrop.py)

![CustomWidgetSortItem](ScreenShot/DragDrop.gif)