# -*- coding: UTF-8 -*-
"""下载管理窗口"""
import pathlib
from collections import OrderedDict
from framework import objects
from framework import fontmgr
from framework import slot
from tools import idm
from tools import urltreemgr
from tools import configmgr

g_FilePath = pathlib.Path(".")
g_fileName = ""
g_fileMoved = False

g_taskData = []

g_workPath = pathlib.Path(configmgr.Load(configmgr.WORK_SPACE, '.'))


@fontmgr.SetFont(fontmgr.SIMHEI_16)
def ShowMainTab():
    """主窗口"""
    initData()
    initCB()
    is_expand, show_custom_window = objects.TabBegin("下载选择窗口", True)
    if is_expand:
        global g_taskData, g_fileName
        objects.Text(g_fileName)
        if objects.Button("下载"):
            lDownloadDict = getDownloadDict()
            idm.DownloadUrlList(lDownloadDict, str(g_workPath.joinpath(g_fileName)))
            moveTaskFile()

        ShowFileTree(g_taskData)
    objects.TabEnd()


def ShowFileTree(urlTree):
    iCheckBoxID = 0
    for node in urlTree:
        if "select" not in node:
            node["select"] = False

        objects.PushID(iCheckBoxID)
        bClick, bSelect = objects.CheckBox("", node["select"])
        objects.PopID()
        iCheckBoxID += 1

        if bClick:
            setChildrenSelect(node, bSelect)
        objects.SameLine()
        if "children" in node:
            if objects.TreeNode(node["title"]):
                ShowFileTree(node["children"])
                objects.TreePop()
        else:
            objects.Text(node["title"])


def setChildrenSelect(node, bSelect):
    node["select"] = bSelect
    for childNode in node.get("children", []):
        setChildrenSelect(childNode, bSelect)


def getDownloadDict():
    return dfsUrlTreeWithSelect(g_taskData)


def dfsUrlTreeWithSelect(rootList):
    res = OrderedDict()
    for node in rootList:
        if "mediaDownloadUrl" in node and node.get("select", False):
            res[node["title"]] = node["mediaDownloadUrl"]
        if "children" in node:
            res.update(dfsUrlTreeWithSelect(node["children"]))
    return res


g_FolderPath = ""
g_WebUrl = ""


def getWebUrl():
    return configmgr.Load(configmgr.WEB_URL, "")


@objects.Once
def initData():
    urltreemgr.GetMgr().Init(getWebUrl(), "")

    global g_taskData
    g_taskData = configmgr.Load("test", [])


@objects.Once
def initCB():
    slot.DRAG_FILE.Connect(dragFilesCB)


def dragFilesCB(lFileList):
    """TODO: 用另外窗口管理"""
    # 暂时抛弃其它的列表
    global g_FilePath, g_fileMoved
    g_FilePath = pathlib.Path(lFileList[0])
    g_fileMoved = False
    refreshTreeData()


def refreshTreeData():
    global g_fileName, g_taskData
    g_fileName = g_FilePath.name
    g_fileName = g_fileName[:g_fileName.rfind('.')]
    g_taskData = urltreemgr.GetMgr().ParseID(g_fileName)
    sTarget = g_workPath.joinpath(g_fileName)
    sTarget.mkdir(parents=True, exist_ok=True)
    with open(str(g_workPath.joinpath(g_fileName, "{}.cache".format(g_fileName))), "w") as cacheFile:
        cacheFile.write(repr(g_taskData))


def moveTaskFile():
    global g_fileMoved
    if g_fileMoved:
        return
    g_FilePath.replace(g_workPath.joinpath(g_fileName, g_FilePath.name))
    g_fileMoved = True
