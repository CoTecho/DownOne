# -*- coding: UTF-8 -*-
"""界面入口"""
from framework import objects
from . import downloadtab


def Start(dWidth, dHeight):
    objects.ExitButton(dWidth, dHeight)
    downloadtab.ShowMainTab()
