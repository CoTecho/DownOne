# -*- coding: UTF-8 -*-
"""
imgui字体管理器
    调用SetFont装饰器，来使UI可以显示中文
    >>># imgui 显示个中文可真难啊
"""
from functools import wraps
import imgui

# region 字体设置
SIMHEI_16 = 1
SIMHEI_18 = 2
SIMHEI_20 = 3

FONTS_CONFIG = (
    (SIMHEI_16, "simhei.ttf", 16),
    # TODO: Low Effective
    # (SIMHEI_18, "simhei.ttf", 18),
    # (SIMHEI_20, "simhei.ttf", 20),
)


# endregion

def SetFont(sFontName):
    """装饰UI函数，使用特定字体"""

    def wrapper(oUIFunc):
        @wraps(oUIFunc)
        def wrapped(*args, **kwargs):
            oFont = GetMgr().GetFont(sFontName)
            imgui.push_font(oFont)
            res = oUIFunc(*args, **kwargs)
            imgui.pop_font()
            return res

        return wrapped

    return wrapper


g_FontMgr = None


def Clear():
    global g_FontMgr
    g_FontMgr = None


def GetMgr():
    global g_FontMgr
    if not g_FontMgr:
        g_FontMgr = CFontMgr()
    return g_FontMgr


class CFontMgr(object):
    """创建并管理字体"""

    def __init__(self):
        self.m_oImpl = None
        self.m_oFonts = None
        self.m_dFontDict = {}  # 保存创建的字体

    def Init(self, oImpl):
        assert hasattr(oImpl, "refresh_font_texture"), "Need a impl!"
        self.m_oImpl = oImpl
        self.m_oFonts = imgui.get_io().fonts
        for config in FONTS_CONFIG:
            self.Create(*config)

    def Create(self, sFontName, sFontPath, iFontSize=14, oRange=None):
        if not oRange:
            oRange = self.m_oFonts.get_glyph_ranges_chinese_full()
        self.m_dFontDict[sFontName] = self.m_oFonts.add_font_from_file_ttf(
            filename=sFontPath,
            size_pixels=iFontSize,
            glyph_ranges=oRange
        )
        self.m_oImpl.refresh_font_texture()

    def GetFont(self, sFontName):
        oFont = self.m_dFontDict.get(sFontName, None)
        assert oFont is not None, "Create {} before use".format(sFontName)
        return oFont
