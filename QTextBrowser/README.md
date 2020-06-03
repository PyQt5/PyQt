# QTextBrowser

- 目录
  - [动态加载图片](#1动态加载图片)

## 1、动态加载图片
[运行 DynamicRes.py](DynamicRes.py)

动态加载资源有多种方式，这里主要介绍 [addResource](https://doc.qt.io/qt-5/qtextdocument.html#addResource) 和 [loadResource](https://doc.qt.io/qt-5/qtextbrowser.html#loadResource) 函数

1、通过 `self.textBrowser.document().addResource(QTextDocument.ImageResource, QUrl('dynamic:/images/weixin.png'), img)` 向文档中注册新的资源索引，类似QRC
2、通过重载 `loadResource` 函数可以监听到所有的资源加载，然后动态返回内容

![DynamicRes](ScreenShot/DynamicRes.gif)