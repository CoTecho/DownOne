# -*- coding: UTF-8 -*-
"""下载管理窗口"""
from framework import objects
from framework import fontmgr
from tools import idm
from tools import urltreemgr
from tools import configmgr


@fontmgr.SetFont(fontmgr.SIMHEI_16)
def ShowMainTab():
    """主窗口"""
    initData()
    is_expand, show_custom_window = objects.TabBegin("下载选择窗口", True)
    if is_expand:
        if objects.Button("打印"):
            print(urltreemgr.GetMgr().ParseID("******"))
    objects.TabEnd()


g_FolderPath = ""
g_WebUrl = ""


def getWebUrl():
    return configmgr.Load(configmgr.WEB_URL, "")


@objects.Once
def initData():
    urltreemgr.GetMgr().Init(getWebUrl(), "")
    print(getWebUrl())
