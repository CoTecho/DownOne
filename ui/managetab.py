# -*- coding: UTF-8 -*-
from pathlib import Path

import framework.objects
from framework import objects
from framework import memory
from framework import fontmgr
from tools import configmgr
from tools import urlinfomgr

MEDIA_BASE = Path(configmgr.Load(configmgr.MEDIA_BASE, "."))


@fontmgr.SetFont(fontmgr.SIMHEI_16)
def ShowMainTab():
    InitData()
    if objects.TabBegin("库存管理"):
        for fdir in MEDIA_BASE.iterdir():
            # TODO: 用memory管理
            if fdir.is_dir():
                bChanged, bState = objects.CheckBox("##{}".format(fdir.name), memory.SelectDirList.IsDirSelected(fdir))
                objects.SameLine()
                objects.Text("{}".format(fdir.name))
                objects.SameLine()
                dFileInfo = memory.FileInfoDict.GetInfo(fdir.name)
                if not dFileInfo:
                    dFileInfo = urlinfomgr.GetMgr().ParseID(fdir.name)
                    memory.FileInfoDict.SetInfo(fdir.name, dFileInfo)
                if objects.Button("详情##{}".format(fdir.name)):
                    lRes = memory.FileInfoDict.GetSortedList("rate_average_2dp", True)
                    for i in lRes:
                        print("{}, {}".format(i, memory.FileInfoDict.GetInfo(i)["rate_average_2dp"]))

                    for k in dFileInfo:
                        print("{}: {}".format(k, dFileInfo[k]))
                lVas = dFileInfo["vas"]
                for dVa in lVas:
                    objects.SameLine()
                    objects.Text("{}".format(dVa["name"]))
                if bChanged:
                    if bState:
                        memory.SelectDirList.SelectDir(fdir)
                    else:
                        memory.SelectDirList.UnselectDir(fdir)
                # if objects.IsItemHovered():
                #     objects.OpenPopup("{}".format(fdir.name))
                # if objects.BeginPopup("{}".format(fdir.name)):
                #     objects.Text("{}".format(fdir.name))
                #     if not objects.IsWindowHovered():
                #         objects.CloseCurrentPopup()
                #     objects.EndPopup()
        objects.TabEnd()


def ShowDetailTab():
    pass


@framework.objects.Once
def InitData():
    sUrl = configmgr.Load(configmgr.WEB_URL)
    sPath = configmgr.Load(configmgr.MEDIA_BASE)
    urlinfomgr.GetMgr().Init(sUrl, sPath)
