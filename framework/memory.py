# -*- coding: UTF-8 -*-
from tools import configmgr
from framework import slot

# region 全局运行
g_IsMousePassthrough = True
g_TimesStore = {}  # 保存调用次数的装饰器


def SetMousePassthrough(bPassthrough):
    global g_IsMousePassthrough
    g_IsMousePassthrough = bPassthrough
    slot.CHANGE_WINDOW_PASS_THROUGH.Emit(bPassthrough)
    configmgr.Save(configmgr.MOUSE_PASSTHROUGH, bPassthrough)


def GetMousePassthrough():
    return g_IsMousePassthrough


def GetFuncRunTimes():
    return g_TimesStore


# endregion


# 各窗口共享


def Init():
    global g_IsMousePassthrough
    g_IsMousePassthrough = configmgr.Load(configmgr.MOUSE_PASSTHROUGH, "True")
