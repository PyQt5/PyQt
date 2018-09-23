# -*- coding: utf-8 -*-

import os, time, sys , importlib
#__file__ 为此文件路径 , 在ipython里是测不出来的
pluginsManagerPath = os.path.dirname(os.path.abspath(__file__))
#主脚本目录
mainPath           = os.path.dirname(pluginsManagerPath)
#自定义插件目录
pluginsPath        =  os.path.join( mainPath, "Plugins")
#以后可能会有其他插件目录
AllPluginsPath     = {"customer":pluginsPath}
#设置模块搜索路径
for key in AllPluginsPath :
    if AllPluginsPath[key] not in sys.path:
        sys.path.insert(0, AllPluginsPath[key]) 

from copy import deepcopy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PluginManager.PluginStore import PluginStore
from PluginManager.PluginStore.StoreModel import FileModel

from Tools.pmf_myjson import *

"setting_flie -> From Tools.pmf_myjson , json写入的位置"

class PluginManager(QObject):
    startDelJson = pyqtSignal()
    
    def __init__(self, parent=None, *args, **kwargs):
        super(PluginManager, self).__init__(parent, *args, **kwargs)
        self.__mw = parent
        self.__initUI()

        self.startDelJson.connect(self.delJson)
        self.palceBTN = QPushButton("哈哈")
        self.pluginDirs = {"pluginFolder": os.path.join(
        os.path.abspath("./"), 
        "Plugins"), }

        self.header = ["PlugName",
                       "Allow", "CreateTime", "ModifyTime"]

        self.pluginsInfo = {
            "StartModule": {},
        }
        # self.jsonPlugin   :{插件名:{header参数}}

        self.jsonPlugin = None

    def __initUI(self):
        mw = self.__mw
        if mw.findChild(QMenuBar, "menuBar"):

            mw.menuPlugin = QAction("Plugin", self.__mw.menuBar,
                                    triggered=self.__createPluginStoreDialog)

            mw.menuBar.addAction(self.__mw.menuPlugin)

        else:
            QMessageBox.information(mw, "", "主窗体没有菜单栏, 请先创建.")

        # 文件监听器

        self.model = FileModel(self)
        self.model.setRootPath("./Plugins")
        self.model.setFilter(QDir.Files)
        self.model.setNameFilters(["Plugin*.py"])
        self.model.setNameFilterDisables(False);
        self.index = self.model.index("./Plugins")
        
        self.model.directoryLoaded.connect(self.start)
        
#        print(self.model.headerData(1, Qt.Horizontal))
#        self.model.setHeaderData(4, Qt.Horizontal, "长江三角洲 ")
        
    def __createPluginStoreDialog(self):
        """
        显示插件加载情况的 窗体.
        """
        dia = PluginStore.PluginStore(self, self.__mw)

        dia.exec_()        
        
    def m_rowsRemoved(self, index, first, last):
        print("removeName:", self.model.index(first, 0, index).data(),first )
        mod = (self.model.index(first, 0, index).data())[:-3]

        self.pluginsInfo["StartModule"].pop(mod)
        self.delJson({}, self.pluginsInfo["StartModule"])
        self.unload(mod)

    def m_rowsInserted(self, index, first, last):
        print("insertName:", self.model.index(first, 0, index).data(), first)
        f = self.model.index(first, 0, index).data()
        mod = f[:-3]
        fullPath = os.path.join(self.pluginDirs["pluginFolder"], f)
        self.pluginsInfo["StartModule"][mod] = {"path": fullPath}
        self.addJson(fullPath, mod)
        self.load(mod)
#        print("I---", self.pluginsInfo["StartModule"])
        
    def start(self):
        """
        self.model 异步加载完成之后开始调用 self.startGetPlugin.
        """
        self.jsonPlugin = self.startGetPlugin(self.pluginDirs['pluginFolder'])
#        print("jsonPlugin:", self.jsonPlugin,"\n",
#              "pluginsModule:", self.pluginsInfo)
        self.loadAll()
        
        self.model.rowsAboutToBeRemoved.connect(self.m_rowsRemoved)
        self.model.rowsInserted.connect(self.m_rowsInserted)        
        self.model.directoryLoaded.disconnect(self.start)
#        self.__createPluginStoreDialog()
    def startGetPlugin(self, pluginFolder: "./Plugins", CHANGE=False) -> "FoJson":

        """
        程序启动加载模块.
        """
        try:
            jsonPlugin = mfunc_readJson(setting_flie)

        except:
            jsonPlugin = {}

        pluginInfo = {}

        rowCount = self.model.rowCount(self.index)

        for row in range(rowCount):
            index = self.model.index(row, 0, self.index)
            # 文件名
            f = index.data()
            # 去掉后缀 , 加入模块
            module = f[:-3]
            fullPath = os.path.join(pluginFolder, f)

            pluginInfo[module] = {"path": fullPath}
            try:
                if module not in jsonPlugin:
                    self.addJson(fullPath, module)
            except:
                self.addJson(fullPath, module)

        if CHANGE is False:
            self.pluginsInfo["StartModule"] = deepcopy(pluginInfo)

        jsonPlugin = self.delJson(jsonPlugin, pluginInfo)
        
#        print("jsonPlugin",jsonPlugin, "\n",  "pluginInfo",pluginInfo )
        
        return jsonPlugin

    def addJson(self, fullPath, module) -> "ToJson":
        # 插件创建时间
        _ctime = time.localtime(os.stat(fullPath).st_ctime)
        ctime = time.strftime("%Y-%m-%d-%H:%M:%S", _ctime)
        # 插件修改时间
        _mtime = time.localtime(os.stat(fullPath).st_mtime)
        mtime = time.strftime("%Y-%m-%d-%H:%M:%S", _mtime)

        # 写入配置
        mfunc_AKrCVJson(module,
                        {
                            self.header[1]: True,  # allow
                            self.header[2]: ctime,  # cteateTime
                            self.header[3]: mtime,  # modifyTime
                        },
                        self=self)

    def delJson(self, jsonPlugin, pluginInfo) -> "ToJson":

        """
        删除插件 的json配置.
        """
        # 添加完重新加载一遍看是否有插件删除
        if jsonPlugin == {}:
            jsonPlugin = mfunc_readJson(setting_flie)

        if len(jsonPlugin) - len(pluginInfo):
            long, short = jsonPlugin, pluginInfo
        else:
            long, short = pluginInfo, jsonPlugin

        with open(setting_flie, 'a+', encoding='utf-8') as f:
            # 被删除的插件集合
            delPlugin = set(long) - set(short)
            for item in delPlugin:
                jsonPlugin.pop(item)
            # 写入配置
            mfunc_reDumpJson(f, jsonPlugin)
            
        return jsonPlugin
    # 加载所有插件
    def loadAll(self):

        for mod in self.jsonPlugin:
            if self.jsonPlugin[mod]["Allow"]:

                try:
                    self.load(mod)
                except:
                    continue
            else:
                self.pluginsInfo["StartModule"][mod]["active"] = False
        for obj in self.__mw.children():
            if obj.objectName() == "Form":
                
                print(obj.objectName(), 
                dir(obj), obj.__class__,  obj.__dict__)
                print(self.__mw.__dict__)
    # 加载插件
    def load(self, mod: "str"):
        try:
            # 动态载入模块
            _pluginModule = importlib.import_module(mod)
            
        except:
#            QMessageBox.information(self.__mw,
#                                    "模块导入异常",
#                                    "请在%s.py检查模块."%mod)

            self.pluginsInfo["StartModule"][mod]["active"] = False
            
            return False

        try:
            className   = getattr(_pluginModule, "className")
            pluginClass = getattr(_pluginModule,  className )
        except:
            self.pluginsInfo[mod]["active"] = False
            QMessageBox.information(self.__mw,
                                    "插件加载错误",
                                    "请在%s.py全局指定className值." % mod)
            return False
        # 实例化类 
        pluginObject = pluginClass(self.__mw)
        pluginObject.setObjectName(className)
        
        #TODO:其他接口
        
        self.pluginsInfo["StartModule"][mod]["active"] = True

        return True
    
    def reload(self, mod):
        if mod in sys.modules:
            #TODO: 旧对象替换
            importlib.reload(sys.modules[mod])
        else:
            self.load(mod)

    # 卸载插件
    def unload(self, mod: "str"):
        
        if mod in sys.modules:

            self.pluginsInfo["StartModule"][mod]["active"] = False
    
            # TODO: #删除对象
            sys.modules.pop(mod)

        return True
    def replace(self, mod):
        self.__mw.findChild()
#        self.__mw.varticalLayout.replaceWidget( ,self.placeBTN)
        pass
    # 卸载所有插件
    def unloadAll(self):
        pass
        
    def PluginToInterFace(self):
        pass
    
