 # -*- coding: utf-8 -*-
 
import os , time



from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PluginManager import PluginStore

from Tools.pmf_myjson import *

class PluginManager(QObject):

    def __init__(self, parent = None , *args, **kwargs):
        super(PluginManager, self).__init__(parent  , *args, **kwargs)
        self.__mw = parent
        self.__initUI()
        
        self.pluginDirs = {"pluginPath": os.path.join("./", "Plugins"),}
        self.header = ["PlugName","Allow" ,  "CreateTime", "ModifyTime"]
        
#        print("pluginDirs:", os.path.abspath(self.pluginDirs['pluginPath']))

        self.pluginsModel = self.getPluginModules(self.pluginDirs['pluginPath'])

#        print(self.pluginsModel)

    def __initUI(self):
        if self.__mw.findChild(QMenuBar, "menuBar"):
            
            self.__mw.menuPlugin = QAction("Plugin", self.__mw.menuBar, 
                                        triggered = self.__createPluginStoreDialog) 
            self.__mw.menuBar.addAction(self.__mw.menuPlugin) 
            
        else:
            QMessageBox.information(self.__mw, "", "主窗体没有菜单栏, 请先创建.")
    
    def __createPluginStoreDialog(self):
 
        dia = PluginStore.PluginStore(self.header , self.existPlugin , self.__mw)
      
        dia.exec_()
    
    def getPluginModules(self, pluginPath:"./Plugins")->"module list":
        """
        Public method to get a list of plugin modules.
        """
        try:
            existPlugin = mfunc_readJson(setting_flie)
        except:
            existPlugin=[]
            
        pluginFiles = []
        
        for f in os.listdir(pluginPath):
            # 插件名称的有效性检查
            if f.endswith(".py") and f.startswith("Plugin"):
                # 去掉后缀 , 加入模块
                module = f[:-3]
                pluginFiles.append(module)
                # 判断是否存在配置信息中
                if module not in existPlugin:
                    # 插件创建时间
                    _ctime = time.localtime(
                        os.stat(
                            os.path.join( pluginPath , f)
                            ).st_ctime) 
                    ctime = time.strftime("%Y-%m-%d-%H:%M:%S",_ctime)
                    # 插件修改时间
                    _mtime = time.localtime(
                        os.stat(
                            os.path.join( pluginPath , f)
                            ).st_mtime)
                    mtime = time.strftime("%Y-%m-%d-%H:%M:%S",_mtime)
                    # 写入配置
                                        
                    mfunc_writeJson( module , 
                                   {
                                   self.header[1]: True, #allow
                                   self.header[2]: ctime,#cteateTime
                                   self.header[3]: mtime,#modifyTime
                                   } ,  
                                    self = self)
                                    
        # 添加完重新加载一遍看是否有插件删除
        self.delJson(pluginFiles)
        
        return pluginFiles
        
    def delJson(self ,  pluginFiles):  
        
        self.existPlugin = mfunc_readJson(setting_flie)

        if len(self.existPlugin)>len(pluginFiles):
            with open( setting_flie ,'a+' , encoding='utf-8') as f:
                # 被删除的插件集合
                delPlugin = set(self.existPlugin)-set(pluginFiles)
                for item in delPlugin:
                    self.existPlugin.pop(item)
                mfunc_afterDelJson(f, self.existPlugin)
                
    # 加载所有插件
    def loadAll(self):
        pass
 
    # 扫描 JSON 文件中的插件元数据
    def scan(self, path:"str"):
        pass
 
    # 加载插件
    def load(self,  path:"str"):
        pass
 
    # 卸载所有插件
    def unloadAll(self):
        pass
 
    # 卸载插件
    def unload(self,   path:"str"):
        pass
 
    # 获取所有插件
    def plugins(self):
        pass
 
