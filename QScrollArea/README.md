# QScrollArea

- 目录
  - [仿QQ设置面板](#1仿QQ设置面板)

## 1、仿QQ设置面板
[运行 QQSettingPanel.py](QQSettingPanel.py) | [查看 setting.ui](Data/setting.ui)

1. 左侧为`QListWidget`，右侧使用`QScrollArea`设置`QVBoxLayout`，然后依次往里面添加QWidget
2. 右侧添加`QWidget`的时候有两种方案
    1. 左侧list根据序号来索引，右侧添加widget时给定带序号的变量名，如widget_0,widget_1,widget_2之类的，这样可以直接根据`QListWidget`的序号关联起来
    2. 左侧list添加item时给定右侧对应的widget变量值

相关事件：
1. 绑定左侧`QListWidget`的`itemClicked`的到该item的索引
2. 绑定右侧滚动条的`valueChanged`事件得到pos

注意：当`itemClicked`时定位滚动条的值时，需要设置一个标志位用来避免`valueChanged`重复调用item的定位

![QQSettingPanel](ScreenShot/QQSettingPanel.gif)