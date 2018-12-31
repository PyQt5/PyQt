#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@resource:http://blog.csdn.net/zzwdkxx/article/details/39338429
@description: 自定义QEvent事件,上面网址为C++版本原理解释,此篇为python改编
@Created on 2018年3月22日
@email: 625781186@qq.com
'''

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


MyEventType = QEvent.registerEventType(QEvent.User+100)

#//长官

class MyEvent (QEvent):
    def __init__(self, *args, **kwargs):
        super(MyEvent, self).__init__(*args, **kwargs)
        print(MyEventType)
        def QEvent(self,MyEventType):
            pass

#//信使

class MySender(QCoreApplication):

    def __init__(self, *args, **kwargs):
        super(MySender, self).__init__(*args, **kwargs)
    def notify(self, receiver,  event):

        if(event.type() == MyEventType):
        
            print("MyEventType is coming!")
            # //return true;
            # /*这里不能return true,因为重写notify就是在事件被向下传递之前截住它，
            # 随便搞它，搞完了还得给QCoreApplication::notify向下传递，除非在mySender.notify
            # 实现了事件向下传递的那一套。直接返回的话myArmy就收不到这个事件，因为执行完这个
            # mySender.notify的return true后，事件传递被人为的在半截终止了
            # （见Qt事件处理的五个层次http:#//blog.csdn.net/michealtx/article/details/6865891 ）
            # ，下面的myArmy的安装的过滤器和它自己的event都不会收到这个事件，更甭提最后干活
            # 的myEventHandler了。所以在主函数中执行完mySender.sendEvent把myEvent
            # 交给mySender.notify这个败家子儿后，就执行mySender.exec进入其它事件的循环了。这就是
            # 问题http:#//topic.csdn.net/u/20111012/19/78036d16-c163-40f9-a05c-3b7d6f4e9043.html
            # 出现的原因。感谢1+1=2大牛！非常感谢！
            # */
        
        return QCoreApplication.notify(self,receiver, event)

#//军队

class MyArmy (QWidget):

    def MyEventHandler(self,event):

        print("The event is being handled!")
        event.accept()

    def event(self, event):

        if(event.type() == MyEventType):
        
            print("event() is dispathing MyEvent")
            self.MyEventHandler(event)  # //调用事件处理函数
            if(event.isAccepted()):
            
                print("The event has been handled!")
                return True
        return QObject. event(self,event)


#//监控者

class MyWatcher (QObject):

    def eventFilter(self,watched, event):

        if(event.type() == MyEventType):
        
            print("I don't wanna filter MyEventType")
            return False
        
        return QObject.eventFilter(self,watched, event)


if __name__ == "__main__":
    import sys
    #//QCoreApplication a(argc, argv);
    app = QtWidgets.QApplication(sys.argv)
    mySender = MySender(sys.argv)

    myArmy=MyArmy ()
    myWatcher=MyWatcher ()
    myArmy.installEventFilter(myWatcher)  # //安装事件过滤器

    myEvent=MyEvent (MyEventType)
    mySender.sendEvent( myArmy,  myEvent)
    mySender.exec()
