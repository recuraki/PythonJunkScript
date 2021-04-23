import yaml
from pprint import pprint
import os
import sys
from optparse import OptionParser
import rule
import excluder


def argParser():
    arg = {}
    parser = OptionParser()
    parser.add_option("-i", "--in",
                      dest="infilename", default=None)
    parser.add_option("-o", "--out",
                      dest="outfilename", default=None)
    parser.add_option("-r", "--rule",
                      dest="rulefilename",  action=None)
    parser.add_option("-n", "--rulename",
                      dest="rulename",  action=None)

    (options, args) = parser.parse_args()
    arg["infilename"] = options.infilename
    arg["outfilename"] = options.outfilename
    arg["rulefilename"] = options.rulefilename
    arg["rulename"] = options.rulename
    return arg

if __name__ == "__main__":
    # 引数の処理
    args = argParser()
    with open(args["rulefilename"], "r") as fd:
        r = rule.ruleLoader()
        r.load(args["rulefilename"])
    rules = r.rules[args["rulename"]]

    e = excluder.excluder()
    e.loadRule(rules)
    with open(args["infilename"], "r") as fr:
        if args["outfilename"] is None:
            fdsiz = os.path.getsize(args["infilename"])
            e.parse(fr, None, desctiption=args["infilename"], sizefd=fdsiz, tqdmEnable=False)
        else:
            with open(args["outfilename"], "w") as fw:
                fdsiz = os.path.getsize(args["infilename"])
                e.parse(fr, fw, desctiption=args["infilename"], sizefd=fdsiz)


