# -*- coding: UTF-8 -*-
"""下载管理窗口"""
import imgui
from framework import objects
from framework import fontmgr
from tools import idm


@fontmgr.SetFont(fontmgr.SIMHEI_16)
def ShowMainTab():
    """示例中文窗口"""
    is_expand, show_custom_window = imgui.begin("中文窗口", True)
    if is_expand:
        imgui.text("你好")
        imgui.text_ansi("你\033[31m好，世\033[m界 ")
        imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1.0, 0.0)
        imgui.extra.text_ansi_colored("春眠不覺曉，處處聞啼鳥", 0.2, 1.0, 0.0)
    imgui.end()
