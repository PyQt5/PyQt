# 图片加载测试

### [Python3.4.4 or Python3.5][PyQt5]

### 分别通过2种情况加载图片文件和资源文件

1. 通过pyrcc5转换res.qrc为res_rc.py文件，可以直接import加载
 - 转换命令pyrcc5 res.qrc -o res_rc.py
 - import res_rc
 - 此时可以通过QPixmap(":/images/head.jpg")来加载

2. 通过rcc命令转成为二进制文件res.rcc
 - 转换命令cd tools
 - rcc.exe -binary ../res.qrc -o ../res.data
 - 通过QResource.registerResource("res.data")注册
 - 此时可以通过QPixmap(":/images/head.jpg")来加载

3. 文本资源读取

```
def readText(path):
    file = QFile(path)
    if not file.open(QIODevice.ReadOnly):
        return ''
    stream = QTextStream(file)
    #下面这句设置编码根据文件的编码自行确定
    stream.setCodec(QTextCodec.codecForName('UTF-8'))
    data = stream.readAll()
    file.close()
    del stream
    return data
```

其它方式见https://github.com/892768447/PyQt/tree/master/%E5%9B%BE%E7%89%87%E5%8A%A0%E8%BD%BD