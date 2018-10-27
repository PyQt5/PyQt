# .9格式图片显示（气泡）

什么叫.9.PNG呢，这是安卓开发里面的一种特殊的图片
这种格式的图片在android 环境下具有自适应调节大小的能力。


（1）允许开发人员定义可扩展区域，当需要延伸图片以填充比图片本身更大区域时，可扩展区的内容被延展。

（2）允许开发人员定义内容显示区，用于显示文字或其他内容

目前手机QQ中很多漂亮的的聊天气泡就是.9格式的png图片

在Github开源库中搜索到两个C++版本的

1.一个是NinePatchQt https://github.com/Roninsc2/NinePatchQt

2.一个是QtNinePatch https://github.com/soramimi/QtNinePatch

### For PyQt
1、目前针对第一个库在2年前用[纯python版本1](纯python版本1/)参考源码重新写一个见

2、这次针对第二个写了[纯python版本2](纯python版本2/)的和[pyd编译好的](pyd版本)两个版本

### 说明
1、建议优先使用pyd版本的（后续提供Python3.4 3.5 3.6 3.7 编译好的32为库文件），也可以自行编译，编译步骤见下文。

2、其次可以使用纯python版本2的（个人觉得方便调用）

3、最后再考虑纯python版本1的吧

4、以上为个人意见，两个C++版本的写法不一样，但是核心算法应该是类似的。

### 自行编译

1、首先要安装好Qt、PyQt5、编译安装对应的sip、对应的VC++编译工具

2、用Qt Creator 打开pro文件进行编译

3、进入源码中的sip文件夹

4、修改configure.py文件

```python
# 这里是你的VC版本和对应的Qt目录中的文件夹
config.platform = "win32-msvc2010"
qt_path = 'D:/soft/Qt/Qt5.5.1/5.5/msvc2010'
```

5、python configure.py

# 截图

![截图1](ScreenShot/1.gif)
