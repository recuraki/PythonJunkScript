#! env python

from pprint import *

CiscoTest="""
vrf definition Mgmt-intf
 !
 address-family ipv6
  desc hoge
  moge
   mogen
 exit-address-family
interface Loopback1
 ip address 10.10.0.13 255.255.255.255
 ip ospf cost 1
 ipv6 address 2001:DB8:0:10::12/128
 ospfv3 cost 1
 """

isComment = lambda x: x.strip("\r\n ") == "!"

def CountPrefixChars(target, line):
    """
    lineの先頭にtargetが何文字含まれているかをカウントする
    """
    c = 0
    if line == "":
        return 0
    if line[0] == target:
        c = 1 + CountPrefixChars(target, line[1:])
        return c
    else:
        return 0


def ParseText(stText: str):
    liCur = []
    liConfig = []
    for line in stText.split("\n"):
        line = line.rstrip()
        if isComment(line):
            continue
        if line == "":
            continue
        liCur = ParseConf(line, liCur)
        liConfig.append(liCur)
        print(liCur)
    return liConfig


def ParseConf(stLine: str, liPrev = []):
    depthCur = CountPrefixChars(" ", stLine)
    depthPrev = len(liPrev)
    res = liPrev[:depthCur]
    stLine = stLine.strip()
    res.append(stLine)
    if res is not None:
        return res
    else:
        return []

class ConfigTree(object):
    diConfig = {}

    def __init__(self):
        self.diConfig = {}

    def update(self, liConfig: list):
        for stElem in liConfig:
            print("CurDiconfig" + str(self.diConfig))
            r = self.updateRoutine(self.diConfig, stElem)
            self.diConfig.update(r)
        pprint(self.diConfig, depth=10, indent=10)

    def updateRoutine(self, diConfig:dict, liLine: list):
        print("diConfig: " + str(diConfig))
        print("line" + str(liLine))
        stElem = liLine[0]
        liChildElems = liLine[1:]
        if stElem not in diConfig:
            print("終点")
            diConfig[stElem] = {}
        else:
            r = self.updateRoutine(diConfig[stElem], liChildElems)
            diConfig[stElem] = r
        return diConfig

if __name__ == "__main__":
    liConfig = ParseText(CiscoTest)
    print(liConfig)
    print("\n")
    conf1 = ConfigTree()
    conf1.update(liConfig)

