# -*- coding: UTF-8 -*-
"""调用adb管理手机文件"""
from ppadb.client import Client as AdbClient
from tools import configmgr

g_oAdbMgr = None


def GetMgr():
    global g_oAdbMgr
    if not g_oAdbMgr:
        g_oAdbMgr = CAdbMgr()
    return g_oAdbMgr


# Default is "127.0.0.1" and 5037
class CAdbMgr(object):
    # TODO: 导出时替换“\ ”为“ ”，设置newline="\n"  LF
    def __init__(self):
        self.m_oDevice = None
        self.m_sBasePath = ""
        self.m_dIDToFile = {}  # {sID:代表文件}，用于生成Tag.txt
        self.m_dFileList = ""
        self.m_lTabFileList = []
        self._init()

    def _init(self):
        client = AdbClient(host="127.0.0.1", port=5037)
        self.m_oDevice = client.devices()[0]
        self.m_sBasePath = configmgr.Load(configmgr.MEDIA_BASE_IN_PHONE)
        print("建立与安卓存储库连接：{}".format(self.m_sBasePath))
        self.RefreshMediaBase()

    def RefreshMediaBase(self):
        self.m_dIDToFile = {}
        self.m_lTabFileList = []
        sOut = self.m_oDevice.shell("ls -1 {}".format(self.m_sBasePath))
        for sName in sOut.split("\n"):
            if sName.endswith(".txt"):
                self.m_lTabFileList.append("{}/{}".format(self.m_sBasePath, sName))
            elif sName.startswith("RJ"):
                sSubOut = self.m_oDevice.shell("ls -1 {}/{}".format(self.m_sBasePath, sName))
                lAudioFile = []
                for sFileName in sSubOut.split("\n"):
                    if sFileName.endswith((".mp3", ".wav")):
                        # TODO: 考虑是否兼容不规范的文件名
                        lAudioFile.append("{}/{}/{}".format(self.m_sBasePath, sName, sFileName))
                self.m_dIDToFile[sName] = lAudioFile
        print("扫描到{}个文件夹，{}个tab.txt".format(len(self.m_dIDToFile), len(self.m_lTabFileList)))

    def GetAllDirName(self):
        return self.m_dIDToFile.keys()

    def GetAllLabelFile(self):
        return self.m_lTabFileList

    def BuildTabListTxt(self, lID):
        """生成保存的.txt文件"""
        lTxt = []
        for sID in lID:
            if self.m_dIDToFile[sID]:
                sFile = self.m_dIDToFile[sID][0].replace("\\ ", " ")
                lTxt.append(sFile)
        return "\n".join(lTxt)

    def CheckEmpty(self):
        dEmptyFile = []
        for sID in self.m_dIDToFile:
            if not self.m_dIDToFile[sID]:
                print(sID)
                dEmptyFile.append(sID)
        return dEmptyFile

    def _hasCover(self, sID):
        cmd = 'mediainfo --inform="Image;%Cover_Format%" {}'
