# QWebEngineView下载文件

## QT官方自带例子 - 额 官方上没有 ，在本地 Examples\Qt-5.9.1\webenginewidgets\demobrowser 文件夹下。

![截图2](ScreenShot/1.png)

#QWebEngineView的下载请求信号
QWebEngineView().page().profile().downloadRequested.connect(self.on_downloadRequested)

#QWebEngineDownloadItem
下载过程的信号
QWebEngineDownloadItem().downloadProgress.connect(self._downloadProgress)
下载结束的信号
QWebEngineDownloadItem().finished.connect(self._finished)

## 参考文献
https://stackoverflow.com/questions/50164712/how-to-open-download-file-dialog-with-qwebengineview-on-pyqt5
https://stackoverflow.com/questions/38812787/how-to-handle-downloads-in-qwebengine
