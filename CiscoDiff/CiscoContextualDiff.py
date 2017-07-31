#! env python3
# -*- coding: utf-8 -*-

from CiscoParse import ParseText
from CiscoParse import ConfigTree
from CiscoParse import ConfigDiff
from pprint import pprint
import optparse
import yaml
import copy
import sys
import os
import codecs
from CiscoLoadVerifyConfig import CiscoLoadVerifyConfig

TestCaseYaml="""
add:
  "interface Loopback0":
    "desctiption loopback":
  "ip nat translation timeout 600":
del:
"""

class CiscoContextualDiff(object):
    """
    Diffモジュール
    """
    C1 = ""
    C2 = ""
    deled = set()
    added = set()
    debug = False
    def __init__(self, debug = False):
        self.debug = debug

    def dprint(self, s):
        if self.debug:
            pprint(s)
    
    def load(self, file1, file2):
        """
        ファイルをロードする
        かつ、パースを開始
        :param file1:
        :param file2:
        :return:
        """
        f = open(file1)
        self.C1 = f.read()
        f.close()
        f = open(file2)
        self.C2 = f.read()
        f.close()
        self.parse()

    def parse(self):
        """
        読み込んだCiscoConfigを実際にパースする
        ここまでで一セット。
        :return:
        """
        self.dprint("Parse1")
        liConfig = ParseText(self.C1, debug = self.debug)
        self.dprint("Parse2")
        liConfig2 = ParseText(self.C2, debug = self.debug)
        self.dprint("Parse End")
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
            pprint(seDel - self.deled)
            res = False
        if res:
            print("OK: SAME CONFIG")
        else:
            print("!!!!!!!!! NG !!!!!!!!!")

        return res

    def generateDiff(self):
        stRes = ""
        stRes = stRes + "[add]" + "\n"
        x = list(self.generateDiffSub(self.added))
        x.sort()
        stRes = stRes +  "\n".join(x) + "\n"
        stRes = stRes + "[delete]" + "\n"
        x = list(self.generateDiffSub(self.deled))
        x.sort()
        stRes = stRes +  "\n".join(x) + "\n"
        return(stRes)

    def generateDiffSub(self, seList:set):
        liRes = list()
        for elem in seList:
            elem = map(lambda x: x.strip(), elem)
            liRes.append(" | ".join(elem))
        return(liRes)


def set2diff(seInput):
    diRes = {}
    for x in seInput:
        diTmp = diRes
        for y in x:
            diCur = diTmp.get(y, {})
            

def listPack(liInput):
    if len(liInput) == 0:
        return None
    return({liInput[0]: listPack(liInput[1:])})


def treeFromYaml(li, Curli = []):
    for x in li:
        Curli.append(x)

def conf2StrWrap(liData, liLevel = [], liRes = []):
    if isinstance(liData, dict):
        res = []
        for x in liData:
            y = copy.deepcopy(liLevel)
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

def dprint(o):
    if f_verbose:
        pprint(o)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-b", "--BEFOREFILE", dest="fn_before", default="sample_before")
    parser.add_option("-a", "--AFTERFILE", dest="fn_after", default="sample_after")
    parser.add_option("-v", "--VERIFYFILE", dest="fn_verify", default="sample_verify")
    parser.add_option("-g", "--GENERATE", dest="f_creat", action="store_true")
    parser.add_option("-o", "--OUTPUT", dest="fn_creat", default = None)
    parser.add_option("-d", "--DEBUG", dest="f_verbose", action="store_true")


    (options, args) = parser.parse_args()
    fn_before = options.fn_before
    fn_after = options.fn_after
    fn_verify = options.fn_verify
    f_creat = options.f_creat
    f_verbose = options.f_verbose
    fn_creat = options.fn_creat

    c = CiscoContextualDiff(debug = f_verbose)
    c.load(fn_before, fn_after)

    #c.dispdiff()
    if f_creat:
        x = c.generateDiff()
        print(x)
        if fn_creat:
            with open(fn_creat, "w") as fw:
                fw.write(x)
    else:
        with open(fn_verify, 'r') as fp:
            cfg = fp.read()

        p = CiscoLoadVerifyConfig()
        p.loadstr(cfg)
        p.parse()

        seWillAdd = p.getSetAdd()
        if seWillAdd != set():
            dprint("--- Will Add")
            dprint(seWillAdd)
        seWillDel = p.getSetDelete()
        if seWillDel != set():
            dprint("--- Will Del")
            dprint(seWillDel)
        c.verify(seWillAdd, seWillDel)


