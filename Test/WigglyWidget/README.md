# WigglyWidget

## Build

Windows

1. 使用 `QtCreator` 打开项目 `CMakeLists.txt`，勾选对应的Qt版本。
2. 在 `QtCreator` 中通过 `项目`->`构建`->`构建步骤`->`详情` 里勾选 `all` 和 `install`
3. 进入 `PyQtWrapper` 目录，打开`vs cmd`，运行 `python -m pip install -r requirements.txt`
4. `sip-build --verbose --tracing --qmake=你的Qt目录下的qmake.exe路径`，等待编译完成
5. `python TestWigglyWidget.py` 进行测试