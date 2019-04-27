# QWebEngineView

- 目录
  - [获取Cookie](#1、获取Cookie)
  - [和Js交互操作](#2、和Js交互操作)

## 1、获取Cookie
[运行 GetCookie.py](GetCookie.py)

通过`QWebEngineProfile`中得到的`cookieStore`并绑定它的`cookieAdded`信号来得到Cookie

![GetCookie](ScreenShot/GetCookie.png)

## 2、和Js交互操作
[运行 JsSignals.py](JsSignals.py)

通过`qwebchannel.js`和`QWebChannel.registerObject`进行Python对象和Javascript的交互

具体看代码中的注释

![JsSignals](ScreenShot/JsSignals.gif)