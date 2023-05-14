import json
import requests
import re

g_TreeMgr = None


def GetMgr():
    global g_TreeMgr
    if not g_TreeMgr:
        g_TreeMgr = CUrlTreeMgr()
    return g_TreeMgr


def Clear():
    global g_TreeMgr
    g_TreeMgr = None


class CUrlTreeMgr(object):
    """下载链接树管理"""

    def __init__(self):
        self.m_sWebUrl = ""
        self.m_sFolderPath = ""

    def Init(self, sWebUrl, sFolderPath):
        self.m_sWebUrl = sWebUrl
        self.m_sFolderPath = sFolderPath

    def ParseID(self, sID):
        """
        @return: url Tree
        """
        sID = re.findall(r'\d+', sID)[0]
        while True:
            try:
                jsonDict = self._downloadJson(sID)
                print("读取成功！")
                break
            except requests.exceptions.ConnectionError:
                print("重试中。。。")
        jsonDict = self._jsonToTreeDict(jsonDict)
        return jsonDict

    def _downloadJson(self, sID):
        """
        获取文件结构字典
        """
        url = "https://api.{}/api/tracks/{}".format(self.m_sWebUrl, sID)
        res = requests.get(url)
        jsonDict = json.loads(res.content.decode("utf-8"))
        return jsonDict

    def _jsonToTreeDict(self, jsonDict):
        """
        将文件分类存储
        """
        if not jsonDict:
            return []
        typeDict = {}
        res = []
        for sub in jsonDict:
            if sub["type"] == "folder":
                sub["children"] = self._jsonToTreeDict(sub["children"])
                res.append(sub)
            else:
                if sub["type"] not in typeDict:
                    typeDict[sub["type"]] = {
                        "type": "folder",
                        "title": "【合并】" + sub["type"],
                        "children": []
                    }
                typeDict[sub["type"]]["children"].append(sub)
        for _, val in typeDict.items():
            res.append(val)
        return res
