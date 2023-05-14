# -*- coding: UTF-8 -*-
"""界面入口"""
from framework import objects
from . import downloadtab
from . import managetab


def Start(dWidth, dHeight):
    objects.ExitButton(dWidth, dHeight)
    downloadtab.ShowMainTab()
    managetab.ShowMainTab()
