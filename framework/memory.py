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


# region 全局运行
IsMousePassthrough = _CStorage(True)
FuncTimesStore = _CTimeStore({})

# endregion


# region 各窗口共享
DragFileList = _CStorage([])


# endregion

def Init():
    IsMousePassthrough.SetData(_mgr.Load(_mgr.MOUSE_PASSTHROUGH, "True"))
