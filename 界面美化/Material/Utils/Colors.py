#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年2月3日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: Colors
@description: 
'''
from collections import OrderedDict

from PyQt5.QtGui import QColor


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class _Color(QColor):

    def __init__(self, *args, **kwargs):
        super(_Color, self).__init__(*args, **kwargs)
        self._name = "_Color"

    def getOpacity(self, alpha: int = 0.6) -> QColor:
        '''
        #类似CSS中的opacity(0-1)
        #get opacity like css opacity
        :param alpha: 透明度
        '''
        return _Color(self).setAlpha(int(255 * alpha))

    def setAlpha(self, alpha: int) -> QColor:
        """
        #设置透明度并且返回本身
        #set alpha and return self
        """
        super(_Color, self).setAlpha(alpha)
        return self

    def setNamed(self, name):
        self._name = name
        return self

    def __str__(self):
        return "rgba{rgba}".format(rgba=self.getRgb())


class _Base(object):

    @property
    def default(self):
        """
        #默认选择饱和度为500的颜色值
        #choose default saturation(500) value
        """
        try:
            return getattr(self, "C500")
        except Exception as e:
            print(e)
            return QColor(255, 255, 255)

    @classmethod
    def alls(cls):
        return (cls.C50, cls.C100, cls.C200, cls.C300,
                cls.C400, cls.C500, cls.C600, cls.C700,
                cls.C800, cls.C900, cls.A100, cls.A200,
                cls.A400, cls.A700)


class Red(_Base):
    """
    # 红色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#fde0dc").setNamed("C50")
    C100 = _Color("#f9bdbb").setNamed("C100")
    C200 = _Color("#f69988").setNamed("C200")
    C300 = _Color("#f36c60").setNamed("C300")
    C400 = _Color("#e84e40").setNamed("C400")
    C500 = _Color("#e51c23").setNamed("C500")
    C600 = _Color("#dd191d").setNamed("C600")
    C700 = _Color("#d01716").setNamed("C700")
    C800 = _Color("#c41411").setNamed("C800")
    C900 = _Color("#b0120a").setNamed("C900")
    A100 = _Color("#ff7997").setNamed("A100")
    A200 = _Color("#ff5177").setNamed("A200")
    A400 = _Color("#ff2d6f").setNamed("A400")
    A700 = _Color("#e00032").setNamed("A700")


class Pink(_Base):
    """
    # 粉色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#fce4ec").setNamed("C50")
    C100 = _Color("#f8bbd0").setNamed("C100")
    C200 = _Color("#f48fb1").setNamed("C200")
    C300 = _Color("#f06292").setNamed("C300")
    C400 = _Color("#ec407a").setNamed("C400")
    C500 = _Color("#e91e63").setNamed("C500")
    C600 = _Color("#d81b60").setNamed("C600")
    C700 = _Color("#c2185b").setNamed("C700")
    C800 = _Color("#ad1457").setNamed("C800")
    C900 = _Color("#880e4f").setNamed("C900")
    A100 = _Color("#ff80ab").setNamed("A100")
    A200 = _Color("#ff4081").setNamed("A200")
    A400 = _Color("#f50057").setNamed("A400")
    A700 = _Color("#c51162").setNamed("A700")


class Purple(_Base):
    """
    # 紫色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#f3e5f5").setNamed("C50")
    C100 = _Color("#e1bee7").setNamed("C100")
    C200 = _Color("#ce93d8").setNamed("C200")
    C300 = _Color("#ba68c8").setNamed("C300")
    C400 = _Color("#ab47bc").setNamed("C400")
    C500 = _Color("#9c27b0").setNamed("C500")
    C600 = _Color("#8e24aa").setNamed("C600")
    C700 = _Color("#7b1fa2").setNamed("C700")
    C800 = _Color("#6a1b9a").setNamed("C800")
    C900 = _Color("#4a148c").setNamed("C900")
    A100 = _Color("#ea80fc").setNamed("A100")
    A200 = _Color("#e040fb").setNamed("A200")
    A400 = _Color("#d500f9").setNamed("A400")
    A700 = _Color("#aa00ff").setNamed("A700")


class DeepPurple(_Base):
    """
    # 深紫色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#ede7f6").setNamed("C50")
    C100 = _Color("#d1c4e9").setNamed("C100")
    C200 = _Color("#b39ddb").setNamed("C200")
    C300 = _Color("#9575cd").setNamed("C300")
    C400 = _Color("#7e57c2").setNamed("C400")
    C500 = _Color("#673ab7").setNamed("C500")
    C600 = _Color("#5e35b1").setNamed("C600")
    C700 = _Color("#512da8").setNamed("C700")
    C800 = _Color("#4527a0").setNamed("C800")
    C900 = _Color("#311b92").setNamed("C900")
    A100 = _Color("#b388ff").setNamed("A100")
    A200 = _Color("#7c4dff").setNamed("A200")
    A400 = _Color("#651fff").setNamed("A400")
    A700 = _Color("#6200ea").setNamed("A700")


class Indigo(_Base):
    """
    # 靛蓝
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#e8eaf6").setNamed("C50")
    C100 = _Color("#c5cae9").setNamed("C100")
    C200 = _Color("#9fa8da").setNamed("C200")
    C300 = _Color("#7986cb").setNamed("C300")
    C400 = _Color("#5c6bc0").setNamed("C400")
    C500 = _Color("#3f51b5").setNamed("C500")
    C600 = _Color("#3949ab").setNamed("C600")
    C700 = _Color("#303f9f").setNamed("C700")
    C800 = _Color("#283593").setNamed("C800")
    C900 = _Color("#1a237e").setNamed("C900")
    A100 = _Color("#8c9eff").setNamed("A100")
    A200 = _Color("#536dfe").setNamed("A200")
    A400 = _Color("#3d5afe").setNamed("A400")
    A700 = _Color("#304ffe").setNamed("A700")


class Blue(_Base):
    """
    # 蓝色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#e7e9fd").setNamed("C50")
    C100 = _Color("#d0d9ff").setNamed("C100")
    C200 = _Color("#afbfff").setNamed("C200")
    C300 = _Color("#91a7ff").setNamed("C300")
    C400 = _Color("#738ffe").setNamed("C400")
    C500 = _Color("#5677fc").setNamed("C500")
    C600 = _Color("#4e6cef").setNamed("C600")
    C700 = _Color("#455ede").setNamed("C700")
    C800 = _Color("#3b50ce").setNamed("C800")
    C900 = _Color("#2a36b1").setNamed("C900")
    A100 = _Color("#a6baff").setNamed("A100")
    A200 = _Color("#6889ff").setNamed("A200")
    A400 = _Color("#4d73ff").setNamed("A400")
    A700 = _Color("#4d69ff").setNamed("A700")


class LightBlue(_Base):
    """
    # 亮蓝色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#e1f5fe").setNamed("C50")
    C100 = _Color("#b3e5fc").setNamed("C100")
    C200 = _Color("#81d4fa").setNamed("C200")
    C300 = _Color("#4fc3f7").setNamed("C300")
    C400 = _Color("#29b6f6").setNamed("C400")
    C500 = _Color("#03a9f4").setNamed("C500")
    C600 = _Color("#039be5").setNamed("C600")
    C700 = _Color("#0288d1").setNamed("C700")
    C800 = _Color("#0277bd").setNamed("C800")
    C900 = _Color("#01579b").setNamed("C900")
    A100 = _Color("#80d8ff").setNamed("A100")
    A200 = _Color("#40c4ff").setNamed("A200")
    A400 = _Color("#00b0ff").setNamed("A400")
    A700 = _Color("#0091ea").setNamed("A700")


class Cyan(_Base):
    """
    # 青色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#e0f7fa").setNamed("C50")
    C100 = _Color("#b2ebf2").setNamed("C100")
    C200 = _Color("#80deea").setNamed("C200")
    C300 = _Color("#4dd0e1").setNamed("C300")
    C400 = _Color("#26c6da").setNamed("C400")
    C500 = _Color("#00bcd4").setNamed("C500")
    C600 = _Color("#00acc1").setNamed("C600")
    C700 = _Color("#0097a7").setNamed("C700")
    C800 = _Color("#00838f").setNamed("C800")
    C900 = _Color("#006064").setNamed("C900")
    A100 = _Color("#84ffff").setNamed("A100")
    A200 = _Color("#18ffff").setNamed("A200")
    A400 = _Color("#00e5ff").setNamed("A400")
    A700 = _Color("#00b8d4").setNamed("A700")


class Teal(_Base):
    """
    # 蓝绿色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#e0f2f1").setNamed("C50")
    C100 = _Color("#b2dfdb").setNamed("C100")
    C200 = _Color("#80cbc4").setNamed("C200")
    C300 = _Color("#4db6ac").setNamed("C300")
    C400 = _Color("#26a69a").setNamed("C400")
    C500 = _Color("#009688").setNamed("C500")
    C600 = _Color("#00897b").setNamed("C600")
    C700 = _Color("#00796b").setNamed("C700")
    C800 = _Color("#00695c").setNamed("C800")
    C900 = _Color("#004d40").setNamed("C900")
    A100 = _Color("#a7ffeb").setNamed("A100")
    A200 = _Color("#64ffda").setNamed("A200")
    A400 = _Color("#1de9b6").setNamed("A400")
    A700 = _Color("#00bfa5").setNamed("A700")


class Green(_Base):
    """
    # 绿色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#d0f8ce").setNamed("C50")
    C100 = _Color("#a3e9a4").setNamed("C100")
    C200 = _Color("#72d572").setNamed("C200")
    C300 = _Color("#42bd41").setNamed("C300")
    C400 = _Color("#2baf2b").setNamed("C400")
    C500 = _Color("#259b24").setNamed("C500")
    C600 = _Color("#0a8f08").setNamed("C600")
    C700 = _Color("#0a7e07").setNamed("C700")
    C800 = _Color("#056f00").setNamed("C800")
    C900 = _Color("#0d5302").setNamed("C900")
    A100 = _Color("#a2f78d").setNamed("A100")
    A200 = _Color("#5af158").setNamed("A200")
    A400 = _Color("#14e715").setNamed("A400")
    A700 = _Color("#12c700").setNamed("A700")


class LightGreen(_Base):
    """
    # 亮绿色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#f1f8e9").setNamed("C50")
    C100 = _Color("#dcedc8").setNamed("C100")
    C200 = _Color("#c5e1a5").setNamed("C200")
    C300 = _Color("#aed581").setNamed("C300")
    C400 = _Color("#9ccc65").setNamed("C400")
    C500 = _Color("#8bc34a").setNamed("C500")
    C600 = _Color("#7cb342").setNamed("C600")
    C700 = _Color("#689f38").setNamed("C700")
    C800 = _Color("#558b2f").setNamed("C800")
    C900 = _Color("#33691e").setNamed("C900")
    A100 = _Color("#ccff90").setNamed("A100")
    A200 = _Color("#b2ff59").setNamed("A200")
    A400 = _Color("#76ff03").setNamed("A400")
    A700 = _Color("#64dd17").setNamed("A700")


class Lime(_Base):
    """
    # 淡黄绿色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#f9fbe7").setNamed("C50")
    C100 = _Color("#f0f4c3").setNamed("C100")
    C200 = _Color("#e6ee9c").setNamed("C200")
    C300 = _Color("#dce775").setNamed("C300")
    C400 = _Color("#d4e157").setNamed("C400")
    C500 = _Color("#cddc39").setNamed("C500")
    C600 = _Color("#c0ca33").setNamed("C600")
    C700 = _Color("#afb42b").setNamed("C700")
    C800 = _Color("#9e9d24").setNamed("C800")
    C900 = _Color("#827717").setNamed("C900")
    A100 = _Color("#f4ff81").setNamed("A100")
    A200 = _Color("#eeff41").setNamed("A200")
    A400 = _Color("#c6ff00").setNamed("A400")
    A700 = _Color("#aeea00").setNamed("A700")


class Yellow(_Base):
    """
    # 黄色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#fffde7").setNamed("C50")
    C100 = _Color("#fff9c4").setNamed("C100")
    C200 = _Color("#fff59d").setNamed("C200")
    C300 = _Color("#fff176").setNamed("C300")
    C400 = _Color("#ffee58").setNamed("C400")
    C500 = _Color("#ffeb3b").setNamed("C500")
    C600 = _Color("#fdd835").setNamed("C600")
    C700 = _Color("#fbc02d").setNamed("C700")
    C800 = _Color("#f9a825").setNamed("C800")
    C900 = _Color("#f57f17").setNamed("C900")
    A100 = _Color("#ffff8d").setNamed("A100")
    A200 = _Color("#ffff00").setNamed("A200")
    A400 = _Color("#ffea00").setNamed("A400")
    A700 = _Color("#ffd600").setNamed("A700")


class Amber(_Base):
    """
    # 琥珀色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#fff8e1").setNamed("C50")
    C100 = _Color("#ffecb3").setNamed("C100")
    C200 = _Color("#ffe082").setNamed("C200")
    C300 = _Color("#ffd54f").setNamed("C300")
    C400 = _Color("#ffca28").setNamed("C400")
    C500 = _Color("#ffc107").setNamed("C500")
    C600 = _Color("#ffb300").setNamed("C600")
    C700 = _Color("#ffa000").setNamed("C700")
    C800 = _Color("#ff8f00").setNamed("C800")
    C900 = _Color("#ff6f00").setNamed("C900")
    A100 = _Color("#ffe57f").setNamed("A100")
    A200 = _Color("#ffd740").setNamed("A200")
    A400 = _Color("#ffc400").setNamed("A400")
    A700 = _Color("#ffab00").setNamed("A700")


class Orange(_Base):
    """
    # 橙色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#fff3e0").setNamed("C50")
    C100 = _Color("#ffe0b2").setNamed("C100")
    C200 = _Color("#ffcc80").setNamed("C200")
    C300 = _Color("#ffb74d").setNamed("C300")
    C400 = _Color("#ffa726").setNamed("C400")
    C500 = _Color("#ff9800").setNamed("C500")
    C600 = _Color("#fb8c00").setNamed("C600")
    C700 = _Color("#f57c00").setNamed("C700")
    C800 = _Color("#ef6c00").setNamed("C800")
    C900 = _Color("#e65100").setNamed("C900")
    A100 = _Color("#ffd180").setNamed("A100")
    A200 = _Color("#ffab40").setNamed("A200")
    A400 = _Color("#ff9100").setNamed("A400")
    A700 = _Color("#ff6d00").setNamed("A700")


class DeepOrange(_Base):
    """
    # 深橙色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 A100 A200 A400 A700
    """

    C50 = _Color("#fbe9e7").setNamed("C50")
    C100 = _Color("#ffccbc").setNamed("C100")
    C200 = _Color("#ffab91").setNamed("C200")
    C300 = _Color("#ff8a65").setNamed("C300")
    C400 = _Color("#ff7043").setNamed("C400")
    C500 = _Color("#ff5722").setNamed("C500")
    C600 = _Color("#f4511e").setNamed("C600")
    C700 = _Color("#e64a19").setNamed("C700")
    C800 = _Color("#d84315").setNamed("C800")
    C900 = _Color("#bf360c").setNamed("C900")
    A100 = _Color("#ff9e80").setNamed("A100")
    A200 = _Color("#ff6e40").setNamed("A200")
    A400 = _Color("#ff3d00").setNamed("A400")
    A700 = _Color("#dd2c00").setNamed("A700")


class Brown(_Base):
    """
    # 棕色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900
    """

    C50 = _Color("#efebe9").setNamed("C50")
    C100 = _Color("#d7ccc8").setNamed("C100")
    C200 = _Color("#bcaaa4").setNamed("C200")
    C300 = _Color("#a1887f").setNamed("C300")
    C400 = _Color("#8d6e63").setNamed("C400")
    C500 = _Color("#795548").setNamed("C500")
    C600 = _Color("#6d4c41").setNamed("C600")
    C700 = _Color("#5d4037").setNamed("C700")
    C800 = _Color("#4e342e").setNamed("C800")
    C900 = _Color("#3e2723").setNamed("C900")

    @classmethod
    def alls(cls):
        return (cls.C50, cls.C100, cls.C200, cls.C300,
                cls.C400, cls.C500, cls.C600, cls.C700,
                cls.C800, cls.C900)


class Grey(_Base):
    """
    # 灰色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900 1000
    """

    C50 = _Color("#fafafa").setNamed("C50")
    C100 = _Color("#f5f5f5").setNamed("C100")
    C200 = _Color("#eeeeee").setNamed("C200")
    C300 = _Color("#e0e0e0").setNamed("C300")
    C400 = _Color("#bdbdbd").setNamed("C400")
    C500 = _Color("#9e9e9e").setNamed("C500")
    C600 = _Color("#757575").setNamed("C600")
    C700 = _Color("#616161").setNamed("C700")
    C800 = _Color("#424242").setNamed("C800")
    C900 = _Color("#212121").setNamed("C900")
    C1000 = _Color("#000000").setNamed("C1000")

    @classmethod
    def alls(cls):
        return (cls.C50, cls.C100, cls.C200, cls.C300,
                cls.C400, cls.C500, cls.C600, cls.C700,
                cls.C800, cls.C900, cls.C1000)


class BlueGrey(_Base):
    """
    # 蓝灰色
    #数字代表饱和度
    #50 100 200 300 400 500 600 100 800 900
    """

    C50 = _Color("#eceff1").setNamed("C50")
    C100 = _Color("#cfd8dc").setNamed("C100")
    C200 = _Color("#b0bec5").setNamed("C200")
    C300 = _Color("#90a4ae").setNamed("C300")
    C400 = _Color("#78909c").setNamed("C400")
    C500 = _Color("#607d8b").setNamed("C500")
    C600 = _Color("#546e7a").setNamed("C600")
    C700 = _Color("#455a64").setNamed("C700")
    C800 = _Color("#37474f").setNamed("C800")
    C900 = _Color("#263238").setNamed("C900")

    @classmethod
    def alls(cls):
        return (cls.C50, cls.C100, cls.C200, cls.C300,
                cls.C400, cls.C500, cls.C600, cls.C700,
                cls.C800, cls.C900)


class Black(_Base):
    """
    #黑色
    """
    C500 = _Color("black").setNamed("C500")

    @classmethod
    def alls(cls):
        return (cls.C500,)


class White(_Base):
    """
    #白色
    """
    C500 = _Color("white").setNamed("C500")

    @classmethod
    def alls(cls):
        return (cls.C500,)


class Transparent(_Base):
    '''透明'''
    name = "Transparent"

    C500 = _Color("white").setNamed("C500")

    @classmethod
    def alls(cls):
        return (cls.C500,)

    @property
    def default(self):
        return self.C500.getOpacity(0)


class Colors(object):
    RED = Red()    # 红色
    PINK = Pink()    # 粉色
    PURPLE = Purple()    # 紫色
    DEEPPURPLE = DeepPurple()    # 深紫色
    INDIGO = Indigo()    # 靛蓝
    BLUE = Blue()    # 蓝色
    LIGHTBLUE = LightBlue()    # 亮蓝色
    CYAN = Cyan()    # 青色
    TEAL = Teal()    # 蓝绿色
    GREEN = Green()    # 绿色
    LIGHTGREEN = LightGreen()    # 亮绿色
    LIME = Lime()    # 淡黄绿色
    YELLOW = Yellow()    # 黄色
    AMBER = Amber()    # 琥珀色
    ORANGE = Orange()    # 橙色
    DEEPORANGE = DeepOrange()    # 深橙色
    BROWN = Brown()    # 棕色
    GREY = Grey()    # 灰色
    BLUEGREY = BlueGrey()    # 蓝灰色
    BLACK = Black()    # 黑色
    WHITE = White()    # 白色
    TRANSPARENT = Transparent()  # 透明


def alls():
    _ = OrderedDict()
    _["Red"] = Red.alls()    # 红色
    _["Pink"] = Pink.alls()    # 粉色
    _["Purple"] = Purple.alls()    # 紫色
    _["DeepPurple"] = DeepPurple.alls()    # 深紫色
    _["Indigo"] = Indigo.alls()    # 靛蓝
    _["Blue"] = Blue.alls()    # 蓝色
    _["LightBlue"] = LightBlue.alls()    # 亮蓝色
    _["Cyan"] = Cyan.alls()    # 青色
    _["Teal"] = Teal.alls()    # 蓝绿色
    _["Green"] = Green.alls()    # 绿色
    _["LightGreen"] = LightGreen.alls()    # 亮绿色
    _["Lime"] = Lime.alls()    # 淡黄绿色
    _["Yellow"] = Yellow.alls()    # 黄色
    _["Amber"] = Amber.alls()    # 琥珀色
    _["Orange"] = Orange.alls()    # 橙色
    _["DeepOrange"] = DeepOrange.alls()    # 深橙色
    _["Brown"] = Brown.alls()    # 棕色
    _["Grey"] = Grey.alls()   # 灰色
    _["BlueGrey"] = BlueGrey.alls()    # 蓝灰色
    return _

# def alls():
#     _colors = {}
#     for colors in dir(Colors):
#         if colors.startswith("_"):
#             continue
#         _Color = getattr(Colors, colors)
#         tmp = []
#         for color in dir(_Color):
#             if color.startswith("_") or color == "default":
#                 continue
#             tmp.append(color)
#         _colors[_Color.__class__] = tmp
#     return _colors

if __name__ == "__main__":
    print(alls().keys())
