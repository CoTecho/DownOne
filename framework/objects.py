# -*- coding: UTF-8 -*-
"""
封装一下imgui的ui控件，项目的ui控件应该从这里拿
"""
import sys
from functools import wraps

import imgui
from framework import fontmgr
from framework import slot

g_TimesStore = {}  # 保存调用次数的装饰器


def Once(oFunc):
    """仅运行一次装饰器"""

    @wraps(oFunc)
    def wrapped(*args, **kwargs):
        if oFunc not in g_TimesStore:
            g_TimesStore[oFunc] = 1
            return oFunc(*args, **kwargs)
        else:
            return

    return wrapped


g_MousePassThrough = True


@fontmgr.SetFont(fontmgr.SIMHEI_16)
def ExitButton(dWidth, dHeight):
    """退出程序"""
    tButtonSize = (68, 25)
    tOffset = (5, 8)

    imgui.set_next_window_bg_alpha(0)
    imgui.begin("Close", False,
                imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_ALWAYS_AUTO_RESIZE)
    global g_MousePassThrough
    vec4ButtonColor = GetStyleColor(imgui.COLOR_BUTTON)
    if g_MousePassThrough:
        vec4ButtonColor = list(vec4ButtonColor)
        vec4ButtonColor[0], vec4ButtonColor[1], vec4ButtonColor[2] = 1, 1, 0
        sLabel = "穿透中"
    else:
        sLabel = "非穿透"
    imgui.push_style_color(imgui.COLOR_BUTTON, *vec4ButtonColor)
    if imgui.button(sLabel, *tButtonSize):
        g_MousePassThrough = not g_MousePassThrough
        slot.CHANGE_WINDOW_PASS_THROUGH.Emit(g_MousePassThrough)
    imgui.pop_style_color()

    imgui.same_line()
    if imgui.button("关闭", *tButtonSize):
        sys.exit()

    tWindowSize = imgui.get_window_size()
    imgui.set_window_position(dWidth - tWindowSize[0] + tOffset[0], 0 - tOffset[1])
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


def GetStyleColor(idx):
    """获取颜色"""
    return imgui.get_style().color(idx)


def Text(sText):
    return imgui.text(sText)


def TreeNode(sLabel, iSetting=0):
    return imgui.tree_node(sLabel, iSetting)


def TreePop():
    return imgui.tree_pop()


def CheckBox(sLabel, bState):
    return imgui.checkbox(sLabel, bState)


def SameLine(iPosition=0, iSpacing=-1):
    return imgui.same_line(iPosition, iSpacing)


def PushID(iID):
    return imgui.push_id(str(iID))


def PopID():
    return imgui.pop_id()
