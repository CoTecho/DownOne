import json
import requests

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
        jsonDict = self._downloadJson(sID)
        jsonDict = self._jsonToTreeDict(jsonDict)
        return jsonDict

    def _downloadJson(self, sID):
        """
        获取文件结构字典
        """
        url = "https://api.{}/api/tracks/{}".format(self.m_sWebUrl, sID)
        res = requests.get(url)
        jsonDict = json.loads(res.content.decode("utf-8"))
        # TODO: save to path
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
                sub["children"] = preBuild(sub["children"])
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


# TODO: imgui style

def preBuild(rjDict):
    """
    将文件分类存储
    """
    if not rjDict:
        return []
    typeDict = {}
    res = []
    for sub in rjDict:
        if sub["type"] == "folder":
            sub["children"] = preBuild(sub["children"])
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


def BuildTreeInner(jsonDict):
    """
    解析获取的字典
    """
    jsonTree.delete(*jsonTree.get_children())
    if "error" in jsonDict:
        print("[ERROR]", jsonDict["error"])
        return
    cnt = 0
    for subDict in jsonDict:
        SubTreeBuilder("", subDict, cnt)
        cnt += 1


def SubTreeBuilder(root, subDict, cnt):
    """
    建立子树
    """
    title = subDict["title"]
    downLoadList = GetDownLoadList(subDict)
    subRoot = jsonTree.insert(root, cnt, text=title, values=downLoadList)
    cnt = 0
    for child in subDict.get("children", []):
        SubTreeBuilder(subRoot, child, cnt)
        cnt += 1


def GetDownLoadList(jsonDict):
    res = []
    root = jsonDict
    if root:
        if root["type"] == "folder":
            for sub in root["children"]:
                res += GetDownLoadList(sub)
        else:
            res.append(root["mediaDownloadUrl"])
    return res
