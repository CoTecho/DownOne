# -*- coding: UTF-8 -*-
"""
模拟内存
    imgui理论上是从内存中取游戏数据然后显示
    仅保存全局变量，不发送信号
"""
from tools import configmgr as _mgr


class _CBaseStorage(object):
    def __init__(self, oDefault=None):
        self.m_oData = oDefault

    def SetData(self, oData):
        self.m_oData = oData

    def GetData(self):
        return self.m_oData


class _CStorage(_CBaseStorage):
    """Normal Storage"""


class _CTimeStore(_CBaseStorage):
    def __init__(self, oDefault=None):
        if oDefault is None:
            oDefault = {}
        assert isinstance(oDefault, dict)
        super(_CTimeStore, self).__init__(oDefault)

    def SetFuncUse(self, oFunc):
        if oFunc not in self.m_oData:
            self.m_oData[oFunc] = 0
        self.m_oData[oFunc] += 1

    def GetFuncTimes(self, oFunc):
        return self.m_oData.get(oFunc, 0)

    def Clear(self):
        self.m_oData = None


class _CDragFileStore(_CBaseStorage):
    def __init__(self, oDefault=None):
        if oDefault is None:
            oDefault = set()
        super().__init__(oDefault)


class _CSelectDirStore(_CBaseStorage):
    def __init__(self, oDefault=None):
        if oDefault is None:
            oDefault = set()
        super().__init__(oDefault)

    def SelectDir(self, oPath):
        self.m_oData.add(oPath)
        print(self.m_oData)

    def IsDirSelected(self, oPath):
        return oPath in self.m_oData

    def UnselectDir(self, oPath):
        if oPath in self.m_oData:
            self.m_oData.remove(oPath)


class _CFileInfoStore(_CBaseStorage):
    def __init__(self, oDefault=None):
        if oDefault is None:
            oDefault = {}
        super().__init__(oDefault)

    def GetInfo(self, sID):
        return self.m_oData.get(sID, {})

    def SetInfo(self, sID, dInfo):
        self.m_oData[sID] = dInfo

    def GetSortedList(self, sKey="id", bReverse=False):
        """排序sID"""
        lRes = self.m_oData.keys()
        lRes = sorted(lRes, key=lambda k: self.m_oData[k][sKey], reverse=bReverse)
        return lRes


# region 全局运行
IsMousePassthrough = _CStorage(True)
FuncTimesStore = _CTimeStore({})

# endregion


# region 各窗口共享
DragFileList = _CStorage([])

SelectDirList = _CSelectDirStore()

FileInfoDict = _CFileInfoStore()


# endregion

def Init():
    IsMousePassthrough.SetData(_mgr.Load(_mgr.MOUSE_PASSTHROUGH, "True"))
