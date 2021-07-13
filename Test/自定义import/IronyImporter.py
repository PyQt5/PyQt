#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年1月28日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: IronyImporter
@description: 
"""
import base64
import os
import sys
from types import ModuleType

import xxtea  # @UnresolvedImport

KEY = base64.b85decode("HF5^hbNbOVOKM=(SB`7h")


class IronyImporter:

    @classmethod
    def find_module(cls, name, path=None):
        name = name + ".irony"
        if not os.path.isfile(name):
            return None
        return cls

    @classmethod
    def load_module(cls, name):
        if name in sys.modules:
            return sys.modules[name]
        mod = ModuleType(name)
        mod.__loader__ = cls
        mod.__name__ = name
        mod.__file__ = name + ".irony"
        try:
            exec(xxtea.decrypt(open(mod.__file__, "rb").read(), KEY), mod.__dict__)
        except Exception as e:
            print(e)
            return None
        sys.modules[name] = mod
        return mod

    @classmethod
    def module_repr(cls, module):
        return "<module {!r} from ({!r})>".format(module.__name__, module.__file__)


sys.meta_path.insert(0, IronyImporter)
