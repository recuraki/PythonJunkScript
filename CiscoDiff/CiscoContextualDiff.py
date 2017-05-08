#! env python3
# -*- coding: utf-8 -*-

from CiscoParse import ParseText
from CiscoParse import ConfigTree
from CiscoParse import ConfigDiff
from pprint import pprint
import optparse
import yaml

TestCaseYaml="""
add:
  "interface Loopback0":
    "desctiption loopback":
  "ip nat translation timeout 600":
del:
"""

class CiscoContextualDiff(object):
    C1 = ""
    C2 = ""
    deled = set()
    added = set()
    def load(self, file1, file2):
        f = open(file1)
        self.C1 = f.read()
        f.close()
        f = open(file2)
        self.C2 = f.read()
        f.close()
        self.parse()

    def parse(self):
        liConfig, liCur1 = ParseText(self.C1)
        liConfig2, liCur2 = ParseText(self.C2)
        Tree1 = set([tuple(x) for x in liConfig])
        Tree2 = set([tuple(x) for x in liConfig2])
        self.deled = Tree1 - Tree2
        self.added = Tree2 - Tree1

    def dispdiff(self):
        print("--- added: ")
        pprint(self.added)
        print("--- deled:")
        pprint(self.deled)
    def verify(self, seAdd, seDel):
        """
        入力した予期する差分とのdiffを取ります。
        :param seAdd: 予期する追加されるべきコマンドセット
        :param seDel: 予期する削除されるべきコマンドセット
        :return: 
        """
        res = True
        if set(self.added - seAdd) != set():
            print("EXTRA-ADD")
            pprint(self.added - seAdd)
            res = False
        if set(seAdd - self.added) != set():
            print("EXPECT ADD BUT NOT ADD")
            pprint(seAdd - self.added)
            res = False
        if set(self.deled - seDel) != set():
            print("EXTRA-DELETE")
            pprint(self.deled - seDel)
            res = False
        if set(seDel - self.deled) != set():
            print("EXPECT DELETE BUT NOT DELETE")
            pprint(seDel - seDel)
            res = False
        return res

def treeFromYaml(li, Curli = []):
    for x in li:
        Curli.append(x)

def conf2StrWrap(liData, liLevel = [], liRes = []):
    if isinstance(liData, dict):
        res = []
        for x in liData:
            y = liLevel.copy()
            y.append(x)
            ret, isEnd = conf2StrWrap(liData[x], y, liRes)
            if isEnd:
                liRes.append(ret)
        return liRes, False

    elif liData == None:
        return liLevel, True

    print("Unreach")

def conf2Str(liData):
    res,y = conf2StrWrap(liData)
    return set([tuple(x) for x in res])



if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-b", "--BEFOREFILE", dest="fn_before", default="sample_before")
    parser.add_option("-a", "--AFTERFILE", dest="fn_after", default="sample_after")
    parser.add_option("-v", "--VERIFYFILE", dest="fn_verify", default="sample_verify")
    (options, args) = parser.parse_args()
    fn_before = options.fn_before
    fn_after = options.fn_after
    fn_verify = options.fn_verify

    c = CiscoContextualDiff()
    c.load(fn_before, fn_after)
    c.dispdiff()
    cfg = yaml.load(TestCaseYaml)
    print("--- Will Add")
    seWillAdd = conf2Str(cfg.get("add", ()))
    pprint(seWillAdd)
    print("--- Will Del")
    seWillDel = conf2Str(cfg.get("del", ()))
    pprint(seWillDel)
    print("---")
    c.verify(seWillAdd, seWillDel)

