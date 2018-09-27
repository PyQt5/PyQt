# -*- coding: utf-8 -*-

"""
增删改查建json.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox , QWidget , QApplication
from PyQt5.QtCore import *

from subprocess import  Popen
import json ,   os


setting_path = "./PluginManager"
setting_Name = "plugin.json"
# 配置文件的路径；
setting_flie = os.path.join(setting_path,  setting_Name)
# 不存在路径就创建文件夹；
if not os.path.exists(setting_path):
    os.makedirs(setting_path)
    if not os.path.exists(setting_path):
        f1 = open(setting_flie, 'a+', encoding='utf-8')
        f1.close()
        
#首次创建 ， 数据默认为name；
name =  {

         }

def mfunc_readJson(f)->"datas":
    '''
    从头读取文件内容。
    '''
    if isinstance(f , str) :
        f = open(setting_flie, 'a+', encoding='utf-8')
    #指针指向；
    f.seek(0)
    #读取；
    text = f.read()
    #json文本转为字典；
    datas= json.loads(text)
    
    f.close()
    #返回python字典
    return datas

def mfunc_initJson( setting_flie ,self=None)->"datas":
    '''
    初始化创建json。
    
    @param setting_flie json路径
    @type str
    '''
    with open( setting_flie ,'a+' , encoding='utf-8') as f:
        
        if self == None:
            self = QWidget()

        try:
            #存在 .json 才能成功；即第二次以后
            datas = mfunc_readJson(f)
        except:
            #首次创建 ， 数据默认为name；
            json.dump( name , f  ,  ensure_ascii=False, indent=1)
            
            try:
                datas = mfunc_readJson(f)
            except:
                QMessageBox.warning(self, 
                        '配置文件格式错误', 
                        '请严格按照JSON格式，\
                        \n解决不了请联系程序员：QQ62578186',
                         QMessageBox.Yes|QMessageBox.No, 
                         QMessageBox.No)
                         
                Popen(["write ", setting_flie])                  
        finally:
            return datas

def mfunc_AKrCVJson( key_name ,  data , self=None):
    '''
    createKey or changeValue。
    
    @param key_name 要修改的json节点的键名
    @type str or list-str

    @param data 新数据
    @type all

    '''
    if self == None:
        self = QWidget()
    
    with open( setting_flie ,'a+' , encoding='utf-8') as f:
        
        datas = mfunc_initJson(setting_flie)
        
#        如果存在键名则替换 ， 不存在则增加
        if isinstance(key_name, str):
            datas[key_name] = data
            
        elif isinstance(key_name, list):
#            TODO:
#            不存在键
            if key_name[0] not in datas:
                                
                msg = QMessageBox.warning(self, 
                '没有找到这个配置节点', 
                "请检查参数格式。\
                \n如果配置不来请清空配置文件。\n是否打开配置文件？",
                QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
                
                if msg==QMessageBox.Yes:
                    Popen(["write ", setting_flie])
                      
                elif msg==QMessageBox.No:
#                    TODO:
                    pass
                return
                
            else:
                # == == == 构造命令文本
                cmd_txt = "datas"
                
                for key in key_name:
                    cmd_txt += (r'''["%s"]'''%key )
                    
                cmd_txt+='=data'
                # == == == 执行命令文本 datas[key]=data
                exec(cmd_txt)
            
        mfunc_reDumpJson(f, datas)

def mfunc_reDumpJson(f , datas):
    # 清空原来的文件
    f.seek(0)
    f.truncate()
    # 写入
    json.dump( datas, f ,  ensure_ascii=False, indent=1)
