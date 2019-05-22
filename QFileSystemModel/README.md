# QFileSystemModel

- 目录
  - [自定义图标](#1自定义图标)

## 1、自定义图标
[运行 CustomIcon.py](CustomIcon.py)

1. 继承 `QFileIconProvider` 类实现自己的图标提供器
2. 重写 `def icon(self, type_info)` 方法根据文件类型返回对应的图标

![CustomIcon](ScreenShot/CustomIcon.png)