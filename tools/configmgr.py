# -*- coding: UTF-8 -*-
from collections import OrderedDict as _dict
from os import path as _path

WEB_URL = "WebUrl"
MEDIA_BASE = "MediaBase"
MOUSE_PASSTHROUGH = "MousePassthrough"
MEDIA_BASE_IN_PHONE = "MediaBaseInPhone"
LRC_BASE = "LrcBase"


def Load(sKey, oDefault=None):
    return GetMgr().Load(sKey, oDefault)


def Save(sKey, oValue):
    GetMgr().Save(sKey, oValue)


CONFIG_PATH = "config.ini"
_Mgr = None


def GetMgr():
    global _Mgr
    if not _Mgr:
        _Mgr = _CMgr()
    return _Mgr


class _CMgr(object):
    PATH = _path.abspath(CONFIG_PATH)

    def __init__(self):
        self.m_dConfig = _dict()
        self._initConfig()

    def _initConfig(self):
        try:
            # exist config file
            with open(self.PATH, encoding="utf-8") as oFile:
                for sLine in oFile:
                    if sLine.strip():
                        sKey, sValue = sLine.split(" = ")
                        self.m_dConfig[sKey] = eval(sValue)
        except FileNotFoundError:
            open(self.PATH, "w", encoding="utf-8").close()
            # TODO: Set Init Config

    def Load(self, sKey, oDefault=None):
        oValue = self.m_dConfig.get(sKey, None)
        return oValue if oValue is not None else oDefault

    def Save(self, sKey, oValue):
        self.m_dConfig[sKey] = oValue
        with open(self.PATH, "w", encoding="utf-8") as oFile:
            sContext = ""
            for k, v in self.m_dConfig.items():
                sContext += "{} = {}\n".format(k, repr(v))
            oFile.write(sContext)
