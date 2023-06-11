# -*- coding: UTF-8 -*-
import json
import requests
import re
import time
from pathlib import Path

g_Mgr = None


def GetMgr():
    global g_Mgr
    if not g_Mgr:
        g_Mgr = CUrlInfoMgr()
    return g_Mgr


def Clear():
    global g_Mgr
    g_Mgr = None


class CUrlInfoMgr(object):
    """详细信息管理"""

    def __init__(self):
        self.m_sWebUrl = ""
        self.m_sFolderPath = Path(".")
        self.m_sCacheFile = Path(".")

    def Init(self, sWebUrl, sFolderPath):
        self.m_sWebUrl = sWebUrl
        self.m_sFolderPath = Path(sFolderPath)

    def ParseID(self, sID):
        """
        @return: url Tree
        """
        self.m_sCacheFile = Path(self.m_sFolderPath.joinpath(sID, "{}.info".format(sID)))
        sID = re.findall(r'\d+', sID)[0]
        jsonDict = {}
        try:
            with open(self.m_sCacheFile, encoding="utf-8") as f:
                jsonDict = eval(f.read())
        except FileNotFoundError:
            print("缓存不存在")
        else:
            print("上次更新：{}".format(time.ctime(jsonDict.get("_UpdateData"))))
        if jsonDict:
            return jsonDict
        while True:
            try:
                jsonDict = self._downloadJson(sID)
                print("读取成功！")
                break
            except requests.exceptions.ConnectionError:
                print("重试中。。。")
        return jsonDict

    def _downloadJson(self, sID):
        """
        获取文件结构字典
        """
        url = "https://api.{}/api/workInfo/{}".format(self.m_sWebUrl, sID)
        res = requests.get(url)
        jsonDict = json.loads(res.content.decode("utf-8"))
        jsonDict["_UpdateData"] = time.time()
        with open(self.m_sCacheFile, "w", encoding="utf-8") as f:
            f.write(repr(jsonDict))
        return jsonDict
