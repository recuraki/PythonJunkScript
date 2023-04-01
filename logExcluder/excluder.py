from typing import NamedTuple
from typing import List, Tuple
from tqdm import tqdm
import sys
from io import StringIO
import unittest
import logging
logging.basicConfig(level=logging.DEBUG)
import re

"""
メモ
- 数十GBのテキストファイルをパースする
- セパレータは"\n"
- メモリ的にreadは一度に行わず、readline
- 時間がかかるので、tqdmで出してやる
- in/outのディスクリプタを与え、適当に処理してやる

exlucde
"""

class Rule(NamedTuple):
    description: str
    action: str
    regcompiled: re.Pattern

actionMap = dict()
actionMap["pass"] = True
actionMap["accept"] = True
actionMap["deny"] = False

unknownFormat = "[UNKNOWN] \033[39m{0} \033[39m"
passFormat = "\033[32m{0} \033[39m"

import io
class excluder(object):
    rules: List[Tuple[str, str, re.Pattern]]

    def __init__(self):
        self.rules = []

    def loadRule(self, rules):
        """
        ルールのロードスクリプト
        ルールを読み込んでreをcompileしとく
        """
        for desc, action, regstr in rules:
            action = action.lower()
            if action not in actionMap:
                logging.warning("rule error:", action)
                continue
            action = actionMap[action]
            regcompiled = None
            try:
                regcompiled = re.compile(regstr)
            except:
                logging.warning("rule error:", regstr)
            self.rules.append(Rule(desc, action, regcompiled))

    def parse(self, fd: io.TextIOWrapper, fw: io.TextIOWrapper, sizefd=None, tqdmEnable = True, desctiption="file", color = False):
        """
        ルールを読み込んで対処する
        """
        import time
        line = "---2"
        # outputするファイルが指定されていないなら、標準出力に出力
        if fw is None:
            fw = sys.stdout
        if tqdmEnable:
            bar = tqdm(total=sizefd)
            bar.set_description(desctiption)
        sizeEnd = 0
        while line != "": # 入力を全て読む
            line = fd.readline()
            isPass = True # 明示的なpassか？
            isKnown = False # 定義されているルールか？
            for _, action, recom in self.rules:
                if recom.match(line):
                    isKnown = True
                    if action: # True = Pass の場合、出力を行う
                        break
                    else: # action = False then deny
                        isPass = False
                        break
            if isKnown:
                if isPass:
                    fw.write(passFormat.format(line))
                    #print(line, file=sys.stderr)
            else: # Unknown
                fw.write(unknownFormat.format(line) )

            sizeEnd += len(line)
            if tqdmEnable:
                bar.update(sizeEnd)


teststr="""
ab
abcd
def
abcdef
"""


if __name__ == "__main__":
    rules = []
    rules.append(("", "pass", "abc"))
    rules.append(("", "deny", "def"))
    obj = excluder()
    obj.loadRule(rules)
    stdout, stdin = sys.stdout, sys.stdin
    sys.stdout, sys.stdin = StringIO(), StringIO(teststr)
    obj.parse(sys.stdin, sys.stdout, sizefd=len(teststr), color=True)
    sys.stdout.seek(0)
    out = sys.stdout.read()[:-1]
    sys.stdout, sys.stdin = stdout, stdin
    print(out)









