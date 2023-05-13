# -*- coding: UTF-8 -*-
"""
封装一下imgui的ui控件，项目的ui控件应该从这里拿
"""
import sys
import imgui
from framework import fontmgr


@fontmgr.SetFont(fontmgr.SIMHEI_16)
def ExitButton(dWidth, dHeight):
    dButtonSize = (68, 25)
    dSpaceSize = (2, 15)
    imgui.set_next_window_bg_alpha(0)
    imgui.begin("Close", False,
                imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR)
    imgui.set_window_position(dWidth - dButtonSize[0] - dSpaceSize[0], 0)
    imgui.set_window_size(dButtonSize[0] + dSpaceSize[0], dButtonSize[1] + dSpaceSize[1])
    if imgui.button("关闭", *dButtonSize):
        sys.exit()
    imgui.end()
