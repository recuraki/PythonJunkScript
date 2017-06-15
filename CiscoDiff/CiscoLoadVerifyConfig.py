#!env python

from pprint import pprint

test = """
[add]
interface Loopback2
interface Loopback2,shutdown
interface Loopback3,shutdown
interface Loopback4
"""

class CiscoLoadVerifyConfig(object):
    configStrAll = ""
    configStrAdd = ""
    configStrDelete = ""

    configSetAdd = set()
    configSetDelete = set()

    sepAdd = "[add]"
    sepDelete = "[delete]"

    def __init__(self):
        pass

    def loadstr(self, s):
        self.configStrAll = s.replace("\r", "")

    def parse(self):
        self.parseSection()
        self.loadSection()

    def loadSection(self):
        self.configSetAdd =  self.loadSectionSub(self.configStrAdd)
        self.configSetDelete =  self.loadSectionSub(self.configStrDelete)

    def getSetAdd(self):
        return self.configSetAdd

    def getSetDelete(self):
        return self.configSetDelete

    def loadSectionSub(self, s:str):
        liRes = []
        for l in s.split("\n"):
            l = l.strip()
            if l == "":
                continue
            liLine = []
            for x in l.split(","):
                liLine.append(x)
            liRes.append(tuple(liLine))
        return set(liRes)


    def parseSection(self):
        """
        [add]と[delete]を切り出す
        :return:
        """
        # [add]などの開始をとる
        posAddStart = self.configStrAll.find(self.sepAdd)
        posDeleteStart = self.configStrAll.find(self.sepDelete)
        # もし、[add]などがなければそのセクションはなくす
        if posAddStart == -1:
            posAddStart = len(self.configStrAll)
        if posDeleteStart == -1:
            posDeleteStart = len(self.configStrAll)
        # [add]などの終わりを表示する。これは次のセクションまで、あるいは、文末までを読み込む
        posAddEnd = posDeleteStart if (posDeleteStart != -1) and (posDeleteStart > posAddStart) else len(self.configStrAll)
        posDeleteEnd = posAddStart if (posAddStart != -1) and (posDeleteStart < posAddStart) else len(self.configStrAll)
        #print("[" + self.configStrAll[posAddStart + 1+ len(self.sepAdd):posAddEnd]+ "]")
        #print("[" + self.configStrAll[posDeleteStart + 1+ len(self.sepDelete):posDeleteEnd] + "]")
        # そのセクションの開始～終了の位置までを各文字列変数にいれる
        # 尚、そのセクションがない場合、は開始が文末になっているので、から文字列になる。
        # ※pythonではstr[n:m](n>m)の場合、""になる。
        self.configStrAdd = self.configStrAll[posAddStart + 1+ len(self.sepAdd):posAddEnd]
        self.configStrDelete =  self.configStrAll[posDeleteStart + 1+ len(self.sepDelete):posDeleteEnd]

if __name__ == "__main__":
    c = CiscoLoadVerifyConfig()
    c.loadstr(test)
    c.parse()