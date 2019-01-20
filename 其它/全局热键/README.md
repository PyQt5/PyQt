# PyQt全局热键 For Windows Test

pip install keyboard

https://github.com/892768447/keyboard

* keyboard
    * 该模块使用全局低级钩子的方式hook键盘来处理,对系统有一定的影响
    * 有反映说弹出对话框假死,这里粗略解决下使用信号槽的方式来弹出对话框
    * 该模块里使用了每次产生一个子线程来回调函数
```
def call_later(fn, args=(), delay=0.001):
    """
    Calls the provided function in a new thread after waiting some time.
    Useful for giving the system some time to process an event, without blocking
    the current execution flow.
    """
    thread = _Thread(target=lambda: (_time.sleep(delay), fn(*args)))
    thread.start()
```

# 截图
![截图](ScreenShot/1.gif)