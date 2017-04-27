#! env python3
# -*- coding: utf-8 -*-

from CiscoParse import ParseText
from CiscoParse import ConfigTree
from CiscoParse import ConfigDiff
from pprint import pprint
import yaml

TestCaseYaml="""
add:
 - "interface Loopback0":
   - "description loopback"
   - "ip ospf cost 10":
     - "hoge"
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
        print("added: ")
        pprint(self.added)
        print("deled:")
        pprint(self.deled)

def treeFromYaml(li, Curli = []):
    for x in li:
        Curli.append(x)


if __name__ == "__main__":
    c = CiscoContextualDiff()
    c.load("sample_before", "sample_after")
    c.dispdiff()

    cfg = yaml.load(TestCaseYaml)
    val = cfg.get("add", {})
    pprint(val)

