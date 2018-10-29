# 简单的子线程例子

使用继承QThread和moveToThread两种方式

# 注意，这里只是简单演示，在应用这些代码时要小心
## 线程的挂起与恢复
这里使用windows的api实现，主要用到SuspendThread和ResumeThread函数

利用ctypes.windll.kernel32.OpenThread(win32con.PROCESS_ALL_ACCESS, False, int(QThread.currentThreadId()))

得到线程的句柄，然后就可以通过上面的两个函数对其进行挂起与恢复

ctypes.windll.kernel32.TerminateThread终止线程，不推荐

## 截图
![截图](ScreenShot/1.gif)