#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import optparse

def usage():
    print "%s <question_file>" % argv[0]

parser = optparse.OptionParser()
parser.add_option("-f", "--FILE", dest="fn_temp")
(options, args) = parser.parse_args()

# 引数処理: 内部変数へのimport
fn_temp = options.fn_temp

if fn_temp == None:
    sys.exit()

liFile = open(fn_temp).read()

if __name__ == '__main__':
    r = liFile.split("~~ End of Syllabus ~~")
    r = "".join(r[1:])
    r = r.split("~~")

    # ok
    r = map(lambda x: x.replace("\n\n", ""), r)
    r = r[1:]

    r = "--\n".join(r)
    print r

    pass
