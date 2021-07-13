import glob
import os
import py_compile
import site
import sys
from distutils.core import setup
from zipfile import ZipFile, ZIP_DEFLATED

sys.argv.append("py2exe")

sitepackages = site.getsitepackages()[1]

py2exe_options = {
    "includes": [],
    "excludes": ["mylibs"],  # 不打包这个
    "dll_excludes": ["MSVCP90.dll", "MSVCR90.dll"],
    "compressed": 1,  # compressed 值为1，则压缩；为0，不压缩，默认为0
    "optimize": 2,  # optimize - 合法值是字符串（'','O','OO'）或者整型数字 (0, 1, or 2)
    "bundle_files": 1
}

setup(
    name="test",
    version="0.0.1",
    console=[
        {"script": "test.py"}
    ],  # 括号中更改为你要打包的代码文件名
    zipfile=None,
    options={'py2exe': py2exe_options},
    data_files=[
        # ("","./icon.ico"),
    ]
)

cores = glob.glob(os.path.join("mylibs", "*.py"))

for core in cores:
    py_compile.compile(
        core, cfile="pyos\\" + core + "o", doraise=True, optimize=2)
print("compile core module ok")

# 添加到压缩文件
zpfd = ZipFile("dist\\mylibs", "w", ZIP_DEFLATED)
zpfd.write("mylibs")

for core in cores:
    zpfd.write("pyos\\" + core + "o", core + "o")
zpfd.close()
print("zip core file ok")

# D:\soft\Python34\python setup.py py2exe

# windows

# console
