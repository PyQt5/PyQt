# -*- coding: utf-8 -*-
"""
管理插件的加载 , 卸载 , 监控文件的添加/删除.
"""
import os, time, sys , importlib, sip, traceback
# ==添加插件的搜索路径==
#__file__ 为此文件路径 , 在ipython里是测不出来的
pluginsManagerPath = os.path.dirname(os.path.abspath(__file__))
#主脚本目录
mainPath           = os.path.dirname(pluginsManagerPath)
#自定义插件目录
pluginsPath        =  os.path.join( mainPath, "Plugins")
pluginsPath2       =  os.path.join( os.path.dirname(sys.argv[0]), "Plugins")
#以后可能会有其他插件目录
AllPluginsPath     = {"customer":pluginsPath, 
                   "afterPacket":pluginsPath2}
#设置模块搜索路径
for key in AllPluginsPath :
    if AllPluginsPath[key] not in sys.path:
        sys.path.insert(0, AllPluginsPath[key]) 
# ==添加插件的搜索路径==

from copy import deepcopy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PluginManager.PluginStore import PluginStore
from PluginManager.PluginStore.StoreModel import FileModel

from Tools.pmf_myjson import *

"setting_flie -> From Tools.pmf_myjson , json写入的位置"

class PluginManager(QObject):
    """
    管理插件的加载 , 卸载 , 监控文件的添加/删除.
    """
    def __init__(self, parent=None, *args, **kwargs):
        super(PluginManager, self).__init__(parent, *args, **kwargs)
        self.__mw = parent
        self.__initUI()

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
            # 插入到mainwindow的menuBar下 , 点击查看弹出插件加载情况窗体===
            mw.menuPlugin = QAction("Plugin", mw.menuBar,
                                    triggered=self.__createPluginStoreDialog)

            mw.menuBar.addAction(mw.menuPlugin)
            
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
                
    def __createPluginStoreDialog(self):
        """
        显示插件加载情况的 窗体.
        """
        if not hasattr(self, "dia"):
            self.dia = PluginStore.PluginStore(self, self.__mw)

        self.dia.show()

    def __m_rowsRemoved(self, index, first, last):
        """
        文件被删除或重命名时候被调用.
        """
        print("removeName:", self.model.index(first, 0, index).data(),first )
        mod = (self.model.index(first, 0, index).data())[:-3]

        self.unload(mod)
        self.pluginsInfo["StartModule"].pop(mod)
        self.delJson(self.jsonPlugin , self.pluginsInfo["StartModule"])  
        
        # pop的步骤u已经在deljson中执行
        # self.jsonPlugin.pop(mod)      
        
    def __m_rowsInserted(self, index, first, last):
        """
        文件增加或重命名时候被调用.
        """
        print("insertName:", self.model.index(first, 0, index).data(), first)
        f = self.model.index(first, 0, index).data()
        mod = f[:-3]
        
        fullPath = os.path.join(self.pluginDirs["pluginFolder"], f)
        self.pluginsInfo["StartModule"][mod] = {"path": fullPath}
        mod, data = self.addJson(fullPath, mod)
        
        self.jsonPlugin[mod] = data
        
        self.load(mod)

    def start(self):
        """
        self.model 异步加载完成之后开始调用 self.startGetPlugin.
        """
        self.jsonPlugin = self.startGetPlugin(self.pluginDirs['pluginFolder'])
#        print("jsonPlugin:", self.jsonPlugin,"\n",
#              "pluginsModule:", self.pluginsInfo)
        self.loadAll()
        
        self.model.rowsAboutToBeRemoved.connect(self.__m_rowsRemoved)
        self.model.rowsInserted.connect(self.__m_rowsInserted)        
        self.model.directoryLoaded.disconnect(self.start)
        self.__createPluginStoreDialog()
        
    def startGetPlugin(self, pluginFolder: "./Plugins", CHANGE=False) -> "FoJson":
        """
        1 . 程序启动加载插件.
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

            if module not in jsonPlugin:
                module, data = self.addJson(fullPath, module)
                jsonPlugin[module]=data


        if CHANGE is False:
            self.pluginsInfo["StartModule"] = deepcopy(pluginInfo)

        jsonPlugin = self.delJson({}, pluginInfo)
        
#        print("jsonPlugin",jsonPlugin, "\n",  "pluginInfo",pluginInfo )
        
        return jsonPlugin

    def addJson(self, fullPath, module) -> "ToJson":
        """
        1.1写入插件 的json配置.
        """
        # 插件创建时间
        _ctime = time.localtime(os.stat(fullPath).st_ctime)
        ctime = time.strftime("%Y-%m-%d-%H:%M:%S", _ctime)
        # 插件修改时间
        _mtime = time.localtime(os.stat(fullPath).st_mtime)
        mtime = time.strftime("%Y-%m-%d-%H:%M:%S", _mtime)
        # 写入配置
        data =  {
                    self.header[1]: True,   # allow
                    self.header[2]: ctime,  # cteateTime
                    self.header[3]: mtime,  # modifyTime
                }
        mfunc_AKrCVJson(module, data , self=self)
        
        return module, data
        
    def delJson(self, jsonPlugin, pluginInfo) -> "ToJson":
        """
        1.2删除插件 的json配置.
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
        """
        2.加载所有模块.
        """
        for mod in self.jsonPlugin:
            if self.jsonPlugin[mod]["Allow"]:
                try:
                    self.load(mod)
                except:
                    continue
            else:
                self.pluginsInfo["StartModule"][mod]["active"] = False
                
    # 加载插件
    def load(self, mod: "str"):
        """
        2.1 载入模块.
        """
        try:
            # 动态载入模块
            _pluginModule = importlib.import_module(mod)
            
        except:
            
            errmsg = traceback.format_exc()
            
            QMessageBox.information(self.__mw,
                                    "模块导入异常",
                                    "%s,请在%s.py检查模块."%(errmsg,mod ))

            self.pluginsInfo["StartModule"][mod]["active"] = False
            
            return False
            
        self.instantiation(mod, _pluginModule)
            
        return True
            
    def instantiation(self , mod, moduleObj , NeedRplace = False):
        """
        2.1.1    实例化类.
        2.2.1.1  
        3.1.1
        实例化新对象来替换旧对象.
        """
        try:
            className   = getattr(moduleObj, "className")
            pluginClass = getattr(moduleObj,  className )
        except:
            self.pluginsInfo["StartModule"][mod]["active"]  = False
            errmsg = traceback.format_exc()  
            QMessageBox.information(self.__mw,
                                    "插件加载错误",
                                    "%s ,请在%s.py全局指定className值." % (errmsg, mod))
            return False            
        # 如果是替换对象需求 ,和初始化
            
        # 实例化类 
        try:
            pluginObject = pluginClass(self.__mw)
            pluginObject.setObjectName(mod)
    
            self.pluginsInfo["StartModule"][mod]["active"]      = True
            self.pluginsInfo["StartModule"][mod]["pluginClass"] = pluginClass
            self.pluginsInfo["StartModule"][mod]["parent"]      = pluginObject.parent()
        except:

            self.pluginsInfo["StartModule"][mod]["active"]  = False
            errmsg = traceback.format_exc()  
            QMessageBox.information(self.__mw,
                                    "插件加载错误",
                                    "%s ,请在%s.py全局指定className值." % (errmsg, mod))
        
        if  not NeedRplace:
            #TODO:其他接口
            layout = pluginObject.getParentLayout()
            pluginObject.toInterface()
            self.pluginsInfo["StartModule"][mod]["layout"] = layout
            self.pluginsInfo["StartModule"][mod]["old"] = pluginObject
        else:
            self.pluginsInfo["StartModule"][mod]["new"] = pluginObject
            return pluginObject
            
    # 重载插件
    def reload(self, mod):
        """
        2.2 重载插件.
        """
        if mod in sys.modules:
            #TODO: 旧对象替换
            print("reload")
            importlib.reload(sys.modules[mod])
            moduleObj = sys.modules[mod]
            try:
                objInfo = self.findOldObj(mod, moduleObj , True)
            except:
                errmsg = traceback.format_exc()
                
                QMessageBox.information(self.__mw,
                                        "模块导入异常",
                                        "%s,请在%s.py检查模块."%(errmsg,mod ))
                
            oldObj, newObj, layout = objInfo["oldObj"],\
                                     objInfo["newObj"],\
                                     objInfo["layout"]
                                     
            # 新对象替换旧对象 ， 并把地址赋值给旧对象
            layout.replaceWidget(oldObj, newObj )
            self.pluginsInfo["StartModule"][mod]["old"] = newObj
            oldObj.flag="reload"
            sip.delete(oldObj)
        else:
            self.load(mod)
    
    def findOldObj(self, mod, moduleObj=None,  needRplace = False):
        """
        3.1
        2.2.1
        找到需要删除或替换的对象.
        """
        oldObj       = self.pluginsInfo["StartModule"][mod]["old"]
        parentWidget = self.pluginsInfo["StartModule"][mod]["parent"]
        layout       = self.pluginsInfo["StartModule"][mod]["layout"]
        pluginClass  = self.pluginsInfo["StartModule"][mod]["pluginClass"]
        if needRplace:
            if moduleObj==None:
                QMessageBox.information(self.__mw,
                        "错误",
                        "请传入moduleObj值.")
            else:
                newObj = self.instantiation(mod, moduleObj, needRplace)
        else:
            newObj = None
            
        return {
                "oldObj"      :oldObj , 
                "newObj"      :newObj ,  
                "parentWidget":parentWidget, 
                "layout"      :layout, 
                "pluginClass" :pluginClass, 
                }
            
    # 卸载插件
    def unload(self, mod: "str"):
        """
        3. 卸载插件 , 移除模块.
        """
        if mod in sys.modules:
            self.pluginsInfo["StartModule"][mod]["active"] = False
            #删除对象
            objInfo = self.findOldObj(mod)
            oldObj  = objInfo["oldObj"] 
            oldObj.flag="unload"
            sip.delete(oldObj)

            self.pluginsInfo["StartModule"][mod]["old"] = None
            sys.modules.pop(mod)
        
        return True
        
    # 卸载所有插件
    def unloadAll(self):
        pass
        
    def PluginToInterFace(self):
        pass
