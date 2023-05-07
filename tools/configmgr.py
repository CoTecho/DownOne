# -*- coding: UTF-8 -*-
from collections import OrderedDict
from os import path


def Load(sKey, oDefault=None):
    return GetMgr().Load(sKey, oDefault)


def Save(sKey, oValue):
    GetMgr().Save(sKey, oValue)


CONFIG_PATH = "config.ini"
g_Mgr = None


def GetMgr():
    global g_Mgr
    if not g_Mgr:
        g_Mgr = CMgr()
    return g_Mgr


class CMgr(object):
    PATH = path.abspath(CONFIG_PATH)

    def __init__(self):
        self.m_dConfig = OrderedDict()
        self._initConfig()

    def _initConfig(self):
        try:
            # exist config file
            with open(self.PATH) as oFile:
                for sLine in oFile:
                    if sLine.strip():
                        sKey, sValue = sLine.split(" = ")
                        self.m_dConfig[sKey] = eval(sValue)
        except FileNotFoundError:
            open(self.PATH, "w").close()
            # TODO: Set Init Config

    def Load(self, sKey, oDefault=None):
        oValue = self.m_dConfig.get(sKey, None)
        return oValue if oValue is not None else oDefault

    def Save(self, sKey, oValue):
        self.m_dConfig[sKey] = oValue
        with open(self.PATH, "w") as oFile:
            sContext = ""
            for k, v in self.m_dConfig.items():
                sContext += "{} = {}\n".format(k, repr(v))
            oFile.write(sContext)
