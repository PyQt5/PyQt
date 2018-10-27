# QListWidget 拖拽、框选

```python
# 隐藏横向滚动条
self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
# 不能编辑
self.setEditTriggers(self.NoEditTriggers)
# 开启拖功能
self.setDragEnabled(True)
# 只能往外拖
self.setDragDropMode(self.DragOnly)
# 忽略放
self.setDefaultDropAction(Qt.IgnoreAction)
# ****重要的一句（作用是可以单选，多选。Ctrl、Shift多选，可从空白位置框选）****
# ****不能用ExtendedSelection,因为它可以在选中item后继续框选会和拖拽冲突****
self.setSelectionMode(self.ContiguousSelection)
# 设置从左到右、自动换行、依次排列
self.setFlow(self.LeftToRight)
self.setWrapping(True)
self.setResizeMode(self.Adjust)
# item的间隔
self.setSpacing(5)
# 橡皮筋(用于框选效果)
self._rubberPos = None
self._rubberBand = QRubberBand(QRubberBand.Rectangle, self)
```

## 拖动Item
```python
# 实现拖拽的时候预览效果图
# 这里演示拼接所有的item截图(也可以自己写算法实现堆叠效果)
def startDrag(self, supportedActions):
    items = self.selectedItems()
    drag = QDrag(self)
    mimeData = self.mimeData(items)
    # 由于QMimeData只能设置image、urls、str、bytes等等不方便
    # 这里添加一个额外的属性直接把item放进去,后面可以根据item取出数据
    mimeData.setProperty('myItems', items)
    drag.setMimeData(mimeData)
    pixmap = QPixmap(self.viewport().visibleRegion().boundingRect().size())
    pixmap.fill(Qt.transparent)
    painter = QPainter()
    painter.begin(pixmap)
    for item in items:
        rect = self.visualRect(self.indexFromItem(item))
        painter.drawPixmap(rect, self.viewport().grab(rect))
    painter.end()
    drag.setPixmap(pixmap)
    drag.setHotSpot(self.viewport().mapFromGlobal(QCursor.pos()))
    drag.exec_(supportedActions)
```

## 模拟框选
```python
def mousePressEvent(self, event):
    # 列表框点击事件,用于设置框选工具的开始位置
    super(DragListWidget, self).mousePressEvent(event)
    if event.buttons() != Qt.LeftButton or self.itemAt(event.pos()):
        return
    self._rubberPos = event.pos()
    self._rubberBand.setGeometry(QRect(self._rubberPos, QSize()))
    self._rubberBand.show()

def mouseReleaseEvent(self, event):
    # 列表框点击释放事件,用于隐藏框选工具
    super(DragListWidget, self).mouseReleaseEvent(event)
    self._rubberPos = None
    self._rubberBand.hide()

def mouseMoveEvent(self, event):
    # 列表框鼠标移动事件,用于设置框选工具的矩形范围
    super(DragListWidget, self).mouseMoveEvent(event)
    if self._rubberPos:
        pos = event.pos()
        lx, ly = self._rubberPos.x(), self._rubberPos.y()
        rx, ry = pos.x(), pos.y()
        size = QSize(abs(rx - lx), abs(ry - ly))
        self._rubberBand.setGeometry(
            QRect(QPoint(min(lx, rx), min(ly, ry)), size))
```

## 截图
![截图](ScreenShot/1.gif)