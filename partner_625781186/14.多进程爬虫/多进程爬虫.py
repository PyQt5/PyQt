import sys
import cgitb
sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

from multiprocessing import Process, Pool

def runPool( i):
    print(i)
    t= py_process()
    t.run()
    
class SWebEngineView(QWebEngineView):
    '''
    浏览器类。
    '''
    def __init__(self, parent=None, url=""):
        super(SWebEngineView, self).__init__()
        self.parent = parent
        self.url = url#初始路径
        self.tempurl=""#组成跳转链接的临时路径
        self.loadFinished.connect(self.gethtml)
        self.show()
        self.a=0
    def gethtml(self, *a, **b):
        self.a+=1
        print("times:", self.a,"--" , self.page().url())
        
    def closeEvent(self,e):
        self.deleteLater()
    def clickLieBiao(self):
        
        print("end")
        
        # title
        self.page().runJavaScript('''$("#alarmtitle").text()''',
                                          self.get_title)
        # content
        self.page().runJavaScript('''$("#alarmcontent").text()''',
                                          self.get_content)
        # datetime re.sub
        self.page().runJavaScript('''$("div.RecoveryDirectoryNav").text()''',
                                          self.get_datetime)
        # img
        self.page().runJavaScript('''$("#alarmimg").attr("src")''',
                                          self.get_img)
    
    def get_title(self, balance):
        # self._dict["title"] = balance

        self.appInList(balance)

    def get_content(self, balance):
        # self._dict["content"] = balance

        self.appInList(balance)

    def get_datetime(self, balance):
        # balance = re.sub(r"【.+?】", "", balance)
        # self._dict["datetime"] = balance

        self.appInList(balance)

    def get_img(self, balance):
        # self._dict["img"] = balance
        self.appInList(balance)
    
    def appInList(self,blance):
        
        print(blance)
        
class py_process(Process):
    def __init__(self):
        super(py_process, self).__init__()
        print("1")
        self.url= r'https://siteserver.progressivedirect.com/session/setidredirect/?&product=AU&statecode=DC&type=New&refer=PGRX&URL=https://qad.progressivedirect.com/ApplicationStart.aspx?Page=Create&OfferingID=DC&state=DC&zip=20007&SessionStart=True'
        self.app = QApplication(sys.argv)
        
        self.browser = SWebEngineView(self, self.url)


    def run(self):         
        print("run1")
        self.browser.setUrl(QUrl(self.url))
        print("run2")
        
        self.app.exec_()

if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    #pool只能在if __name__ == "__main__":中使用
    # pool = Pool(3)
    
    # for i in range(2):
        # pool.apply_async(runPool, (i, ))

    # pool.close()
    # pool.join()
    import os
    os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9000"
    
    # url= r'https://siteserver.progressivedirect.com/session/setidredirect/?&product=AU&statecode=DC&type=New&refer=PGRX&URL=https://qad.progressivedirect.com/ApplicationStart.aspx?Page=Create&OfferingID=DC&state=DC&zip=20007&SessionStart=True'
    url= r'http://www.progressive.com'

    browser = SWebEngineView(url)
        
    print("run1")
    browser.setUrl(QUrl(url))
    print("run2")
        
    sys.exit(app.exec_())
    
