#! env python3
# -*- coding: utf-8 -*-

from pprint import *
import sys

CiscoTest1="""
vrf definition Mgmt-intf
 !
 address-family ipv4
  exit-address-family
 address-family ipv6
  desc hoge
 exit-address-family
interface Loopback1
 ip address 10.10.0.13 255.255.255.255
 ip ospf cost 1
 ipv6 address 2001:DB8:0:10::12/128
 ospfv3 cost 1
 """

CiscoTest2="""
vrf definition Mgmt-intf
 !
 address-family ipv6
  desc moge
 exit-address-family
interface Loopback2
 ip address 10.10.0.13 255.255.255.255
 """

# コメントのみの行か判定
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


def ParseText(stText: str, debug = False):
    """
    コンフィグテキストをパースする関数
    各行を「階層」とともにパースする
    階層とは
    address-family ipv4
     exit-address-family
    のとき"address-family ipv4"の改装の下に"exit-address-family"がいる
    """
    liCur = []
    # 今の「階層」
    liConfig = []
    # 各行を読み込む
    for line in stText.split("\n"):
        # \r\n, \nの正規化のために右側をstrip
        line = line.rstrip()
        # commentのみの行はとばす(!飲みの行)
        if isComment(line):
            continue
        # 空白はとばす
        if line == "":
            continue
        # テキストの行をパースするこの際、今の改装を渡す
        liCur = ParseConf(line, liCur)
        # 戻りをコンフィグ一覧に追加
        liConfig.append(liCur)
        if debug:
            print(liCur)
    return liConfig, liCur

def ParseConf(stLine: str, liPrev = []):
    # 新しい階層を調べる。これはスペースの数
    depthCur = CountPrefixChars(" ", stLine)
    # 現在の改装を調べる
    depthPrev = len(liPrev)
    # 「現在の改装」の「新しい階層」までをfetchする
    res = liPrev[:depthCur]
    # パースに際して空白を除去
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

    def update(self, liConfig: list, debug = False):
        for stElem in liConfig:
            r = self.updateRoutine(self.diConfig, stElem)
            self.diConfig.update(r)
        if debug:
            pprint(self.diConfig, depth=10, indent=10)

    def updateRoutine(self, diConfig:dict, liLine: list):
        if liLine == []:
            return {}
        stElem = liLine[0]
        liChildElems = liLine[1:]
        if stElem not in diConfig:
            diConfig[stElem] = {}
        else:
            r = self.updateRoutine(diConfig[stElem], liChildElems)
            diConfig[stElem] = r
        return diConfig

    def getConfigDict(self):
        return self.diConfig



def lineList2Strs(liLevel: list):
    s = ""
    for lv in  range(0, len(liLevel)):
        s = s + " " * lv + liLevel[lv] + "\n"
    return s


class ConfigDiff(object):
    before = dict()
    after = dict()

    def __init__(self, before: ConfigTree, after: ConfigTree):
        self.before = before.getConfigDict()
        self.after = after.getConfigDict()

    def diff(self):
        self.diff_remove(self.before, self.after)
        self.diff_add(self.before, self.after)

    def diff_remove(self, before: dict, after: dict, liLevel: list = []):
        for stElem in before:
            if stElem not in after:
                #もし、afterに存在しないものであれば
                print(lineList2Strs(liLevel).rstrip())
                print(" " * len(liLevel) + "no " + stElem)
                print("end")
            else:
                self.diff_remove(before[stElem], after[stElem], liLevel + [stElem])


    def diff_add(self, before: dict, after: dict, liLevel: list = []):
        for stElem in after:
            if stElem not in before:
                # もし、afterに存在しないものであれば
                print(lineList2Strs(liLevel).rstrip())
                print(" " * len(liLevel)  + stElem)
                print("end")
                self.diff_add({}, after[stElem], liLevel + [stElem])
            else:
                self.diff_add(before[stElem], after[stElem], liLevel + [stElem])

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        f = open(args[1])
        CiscoTest1 = f.read()
        f.close()
        liConfig, liCur = ParseText(CiscoTest1)
        conf1 = ConfigTree()
        conf1.update(liConfig)

    if len(args) == 3:
        f = open(args[1])
        CiscoTest1 = f.read()
        f.close()
        f = open(args[2])
        CiscoTest2 = f.read()
        f.close()
        liConfig, liCur1 = ParseText(CiscoTest1)
        liConfig2, liCur2 = ParseText(CiscoTest2)
        conf1 = ConfigTree()
        conf1.update(liConfig)
        conf2 = ConfigTree()
        conf2.update(liConfig2)
        ConfigD = ConfigDiff(conf1, conf2)
        ConfigD.diff()


