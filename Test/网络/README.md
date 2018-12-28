# 网络

## [1、控制小车](控制小车/)
通过TCP连接树莓派控制小车的简单例子

需求：

 - 通过TCP连接到树莓派控制小车前后左右
 - 前进：0-100， 发送命令为F:2
 - 后退：0-100， 发送命令为B:2
 - 向左：32-42， 发送命令为L:2
 - 向右：42-52， 发送命令为R:2

注意：

 - 这里只用了UI文件做界面，并没有转换为python代码
 - server.py只是做个本地echo服务器用来测试命令是否正常，依赖`tornado`库，可以通过`pip install tornado`来安装
 - 另外需要做粘包处理，以（\n）作为粘包符
 - 由于wifi能力不行,发送图片要尽量小

说明：

 - `QTcpSocket.connected`    服务连接成功后触发该信号
 - `QTcpSocket.disconnected` 服务器丢失连接触发该信号
 - `QTcpSocket.readyRead`    服务器返回数据触发该信号
 - `QTcpSocket.error`        连接报错触发该信号（连接超时、服务器断开等等）

<font color="red">目前暂未修复接收图片异，原因在于`readyRead`中没有判断数据长度进行多次接收（类似粘包处理）</font>

![截图](控制小车/ScreenShot/控制小车.png)

## [2、窗口配合异步Http](窗口配合异步Http/)
`asyncio`结合PyQt例子

1. 依赖库：
    1. `quamash`（对QT事件循环的封装替换）：https://github.com/harvimt/quamash
    2. `asyncio`：https://docs.python.org/3/library/asyncio.html
    3. `aiohttp`：https://aiohttp.readthedocs.io/en/stable/

2. 在创建`QApplication`后随即设置替换事件循环loop
```python
app = QApplication(sys.argv)
loop = QEventLoop(app)
asyncio.set_event_loop(loop)
w = Window()
```

3. 通过`asyncio.ensure_future(函数(), loop=loop)`来执行某个异步函数

Window　　→→　　initSession（初始化session）

　　↓

　　↓

下载按钮　　→→　　doDownload（执行_doDownload方法）

　　　　　　　　　　　　　　↓

　　　　　　　　　　　　　　↓

　　　　　　　　　　session.get（下载json数据进行解析）

　　　　　　　　　　　　　　↓

　　　　　　　　　　　　　　↓

添加到界面　　←←　　_doDownloadImage（对单张图片进行下载）

![截图](窗口配合异步Http/ScreenShot/窗口配合异步Http.gif)