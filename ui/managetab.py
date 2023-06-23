# -*- coding: UTF-8 -*-
from pathlib import Path

import framework.objects
from framework import objects
from framework import memory
from framework import fontmgr
from tools import configmgr
from tools import urlinfomgr
from tools import albumcover

MEDIA_BASE = Path(configmgr.Load(configmgr.MEDIA_BASE, "."))
g_lShowingDir = []


@fontmgr.SetFont(fontmgr.SIMHEI_16)
def ShowMainTab():
    global g_lShowingDir
    InitData()
    if objects.TabBegin("库存管理"):
        if objects.Button("刷新") or not g_lShowingDir:
            g_lShowingDir = [x for x in MEDIA_BASE.iterdir()]
            print(g_lShowingDir)
        for fdir in g_lShowingDir:
            # TODO: 用memory管理
            if fdir.is_dir():
                # 读取配置
                dFileInfo = memory.FileInfoDict.GetInfo(fdir.name)
                if not dFileInfo:
                    dFileInfo = urlinfomgr.GetMgr().ParseID(fdir.name)
                    memory.FileInfoDict.SetInfo(fdir.name, dFileInfo)
                # region UI代码
                bChanged, bState = objects.CheckBox("##{}".format(fdir.name), memory.SelectDirList.IsDirSelected(fdir))
                objects.SameLine()
                objects.Text("{}".format(fdir.name))
                objects.SameLine()
                bClickInfo = objects.Button("详情##{}".format(fdir.name))
                lVas = dFileInfo["vas"]
                for dVa in lVas:
                    objects.SameLine()
                    objects.Text("{}".format(dVa["name"]))
                # endregion
                # region 逻辑代码
                if bChanged:
                    if bState:
                        memory.SelectDirList.SelectDir(fdir)
                    else:
                        memory.SelectDirList.UnselectDir(fdir)
                if bClickInfo:
                    lRes = memory.FileInfoDict.GetSortedList("rate_average_2dp", True)
                    for k in dFileInfo:
                        # TODO: 可视化
                        print("{}: {}".format(k, dFileInfo[k]))

                bCover = dFileInfo.get("LocalCover", False)
                if not bCover:
                    bCover = albumcover.AutoAddCover(fdir)
                    dFileInfo["LocalCover"] = bCover
                    urlinfomgr.GetMgr().SaveInfo(fdir.name, dFileInfo)
                # endregion
                # 完成处理，保存配置
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
