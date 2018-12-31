# v1.2
# created
#   by Roger
# in 2017.1.3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import configparser


import sys

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle('My Browser')
        # 设置窗口图标
        self.setWindowIcon(QIcon('icons/penguin.png'))
        
        # 设置窗口大小900*600
        self.resize(750, 400)
        self.show()
        self.frame=1
        # 设置浏览器
        self.browser = MyEngineView()
        # config = configparser.ConfigParser()
        # config.readfp(open('url.ini'))
        # url= config.get("URL","url")
        url="http://www.onlinedown.net/soft/56160.htm"
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.browser)

        self.tray = QSystemTrayIcon() #创建系统托盘对象  
        self.icon = QIcon('icons/back.png')  #创建图标  
        self.tray.setIcon(self.icon)  #设置系统托盘图标  
        self.tray.show()


        #使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        #添加导航栏到窗口中
        self.addToolBar(navigation_bar)

        #QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('icons/back.png'), 'Back', self)
        next_button = QAction(QIcon('icons/next.png'), 'Forward', self)
        stop_button = QAction(QIcon('icons/cross.png'), 'stop', self)
        reload_button = QAction(QIcon('icons/renew.png'), 'reload', self)
       
        
        back_button.triggered.connect(self.browser.back)
        next_button.triggered.connect(self.browser.forward)
        stop_button.triggered.connect(self.browser.stop)
        reload_button.triggered.connect(self.browser.reload)
  
        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)
        #添加URL地址栏
        self.urlbar = QLineEdit()
        self.urlbar.setText(url)
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        #让浏览器相应url地址的变化
        self.browser.urlChanged.connect(self.renew_urlbar)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

class MyEngineView(QWebEngineView):
    '''
    浏览器类。
    '''
    def __init__(self, parent=None, ):
        super(MyEngineView, self).__init__(parent)
        self.parent = parent
        #有下载信号发起
        self.page().profile().downloadRequested.connect(self.on_downloadRequested)

    def createWindow(self,  type):
        '''
        实现点击跳转链接。
        '''
        return self  

    #以下函数里的 ：后为注释，无实际作用

        #下载信号连接到的槽
    def on_downloadRequested(self, download : "QWebEngineDownloadItem" ):
        # download是QWebEngineDownloadItem对象；
        download.downloadProgress.connect(self._downloadProgress)
        download.finished.connect(self._finished)

        #下载文件的保存路径及文件名
        old_path = download.path()
        suffix = QFileInfo(old_path).suffix()
        #下载文件类型
        filttype = download.mimeType()
        #后缀切割
        unkonw_suffix = filttype.split(r'/')[-1]
        path, _ =QFileDialog.getSaveFileName(self, "Save File", old_path,  "*."+unkonw_suffix + ";;" + "*."+suffix )

        print(old_path, suffix)

        if path!="":
            download.setPath(path)
            download.accept()

    def _downloadProgress(self , bytesReceived:"qint64", bytesTotal:"qint64"):
        # bytesReceived 当前下载值 ； bytesTotal 文件总大小值
        # self.bytesReceived = bytesReceived
        # self.bytesTotal = bytesTotal
        print(bytesReceived , bytesTotal )

    def _finished(self):
        print("下载完成")

if __name__ == "__main__":
    # 创建应用
    app = QApplication(sys.argv)
    # 创建主窗口
    window = MainWindow()
    # 显示窗口
    window.show()
    # 运行应用，并监听事件
    app.exec_()    
