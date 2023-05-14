# -*- coding: UTF-8 -*-
"""信号槽，用于页面间通信"""
import weakref
import inspect


class CSlot(object):
    def __init__(self):
        self.m_lConnectCB = []

    def Connect(self, oFunc, *args, **kwargs):
        self.m_lConnectCB.append(CFunctor(oFunc, *args, **kwargs))

    def Emit(self, *args, **kwargs):
        for oFunc in self.m_lConnectCB:
            oFunc(*args, **kwargs)


class CFunctor(object):
    """弱引用函数或方法"""

    def __init__(self, oFunc, *args, **kwargs):
        if inspect.isfunction(oFunc):
            self.m_oRef = weakref.ref(oFunc)
        elif inspect.ismethod(oFunc):
            self.m_oRef = weakref.WeakMethod(oFunc)
        else:
            raise TypeError
        self.m_lArgs = args
        self.m_dKwargs = kwargs

    def __call__(self, *args, **kwargs):
        lArgs = self.m_lArgs + args
        self.m_dKwargs.update(kwargs)
        oFunc = self.m_oRef()
        if oFunc:
            return oFunc(*lArgs, **self.m_dKwargs)


DRAG_FILE = CSlot()  # 文件拖拽
CHANGE_WINDOW_PASS_THROUGH = CSlot()  # 窗口穿透
