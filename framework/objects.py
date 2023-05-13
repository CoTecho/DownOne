# -*- coding: UTF-8 -*-
"""
封装一下imgui的ui控件，项目的ui控件应该从这里拿
"""
import sys
import imgui
from framework import fontmgr


@fontmgr.SetFont(fontmgr.SIMHEI_16)
def ExitButton(dWidth, dHeight):
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
