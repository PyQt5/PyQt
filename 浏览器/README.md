# 浏览器

## [1、QWebView](QWebView)

### 1. [梦幻树](QWebView/梦幻树)
在桌面上显示透明html效果，使用`QWebkit`加载html实现,采用窗口背景透明和穿透方式

![截图](QWebView/梦幻树/ScreenShot/梦幻树.png)

### 2. [获取Cookie](QWebView/获取Cookie)
`QWebView`很简单,从`page()`中得到`QNetworkAccessManager`,在从中得到`QNetworkCookieJar`,
最后得到cookie,当然也可以设置自己的`QNetworkCookieJar`

![截图](QWebView/获取Cookie/ScreenShot/获取Cookie.png)

## [2、QWebEngineView](QWebEngineView)

### 1. [获取Cookie](QWebEngineView/获取Cookie)
`QWebEngineView`的话目前是通过`QWebEngineProfile`中得到的`cookieStore`并绑定它的`cookieAdded`信号来得到Cookie

![截图](QWebEngineView/获取Cookie/ScreenShot/获取Cookie.png)