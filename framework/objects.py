# -*- coding: UTF-8 -*-
"""
封装一下imgui的ui控件，项目的ui控件应该从这里拿
"""
import sys
from functools import wraps

import imgui
from framework import fontmgr

g_OnceStore = {}  # 保存记录仅调用一次的装饰器


def Once(oFunc):
    """仅运行一次装饰器"""

    @wraps(oFunc)
    def wrapped(*args, **kwargs):
        if oFunc not in g_OnceStore:
            g_OnceStore[oFunc] = 1
            return oFunc(*args, **kwargs)
        else:
            return

    return wrapped


@fontmgr.SetFont(fontmgr.SIMHEI_16)
def ExitButton(dWidth, dHeight):
    """退出程序"""
    tButtonSize = (68, 25)
    tSpaceSize = (2, 15)
    tOffset = (3, 8)

    imgui.set_next_window_bg_alpha(0)
    imgui.begin("Close", False,
                imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR)
    imgui.set_window_position(dWidth - tButtonSize[0] - tSpaceSize[0] + tOffset[0], 0 - tOffset[1])
    imgui.set_window_size(tButtonSize[0] + tSpaceSize[0], tButtonSize[1] + tSpaceSize[1])
    if imgui.button("关闭", *tButtonSize):
        sys.exit()
    imgui.end()


def TabBegin(sLabel="", bClosable=True, dSetting=0):
    """窗口起始"""
    return imgui.begin(sLabel, bClosable, dSetting)  # | imgui.WINDOW_ALWAYS_AUTO_RESIZE)


def TabEnd():
    """窗口结束"""
    return imgui.end()


def Button(sLabel="", dWidth=0, dHeight=0):
    """基础按钮"""
    return imgui.button(sLabel, dWidth, dHeight)
