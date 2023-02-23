# QMetaObject

- 目录
  - [在线程中操作UI](#1在线程中操作UI)

## 1、在线程中操作UI
[运行 CallInThread.py](CallInThread.py)

如果想在`QThread`或者`threading.Thread`中不通过信号直接操作UI，则可以使用`QMetaObject.invokeMethod`调用。

该函数一般有常用的几种调用方法：

1. 直接调用槽函数：`QMetaObject.invokeMethod(uiobj, 'slot_method', Qt.QueuedConnection)`
2. 直接调用信号：`QMetaObject.invokeMethod(uiobj, 'signal_method', Qt.QueuedConnection)`
3. 调用信号或槽函数并传递参数：`QMetaObject.invokeMethod(uiobj, 'method', Qt.QueuedConnection, Q_ARG(str, 'text'))`
4. 调用槽函数得到返回值：`QMetaObject.invokeMethod(uiobj, 'slot_method', Qt.DirectConnection, Q_RETURN_ARG(str))`
5. 调用带参数的槽函数得到返回值：`QMetaObject.invokeMethod(uiobj, 'slot_method', Qt.DirectConnection, Q_RETURN_ARG(int), Q_ARG(bool, False))`, 传入bool类型的参数，获取int类型返回值

这里需要注意：

1. 调用函数都是异步队列方式，需要使用`Qt.QueuedConnection`
2. 而要得到返回值则必须使用同步方式, 即`Qt.DirectConnection`

![CallInThread](ScreenShot/CallInThread.png)