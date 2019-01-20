# QWebView

## 1、梦幻树
[运行 DreamTree.py](DreamTree.py)
在桌面上显示透明html效果，使用`QWebkit`加载html实现,采用窗口背景透明和穿透方式

![DreamTree](ScreenShot/DreamTree.png)

## 2、获取Cookie
[运行 GetCookie.py](GetCookie.py)

从`page()`中得到`QNetworkAccessManager`,在从中得到`QNetworkCookieJar`,
最后得到cookie,当然也可以设置自己的`QNetworkCookieJar`

![GetCookie](ScreenShot/GetCookie.png)