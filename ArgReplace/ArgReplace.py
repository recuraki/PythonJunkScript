#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import optparse

LineSeparator=","

def usage():
    print "%s <csv_file> <template_file>" % argv[0]

# 最初の１行を処理する
# 以降の行における各列の名前を定義する
def line_proc_first(line):
    # 最初の#をのぞき、空白を削除した文字列をLineSparatorで区切り
    # tmpに代入
    tmp = line[1:].replace(" ", "").split(LineSeparator)
    # 引数の数は区切れた数
    argc = len(tmp)
    return(argc, tmp)



def line_proc_replace(line, argc, argv):
    tmp = line.split(LineSeparator)
    # define al(Argv list)
    al = {}
    for i in range(argc):
        al[argv[i]] = tmp[i]
    print str_template % al

def read_until(fd, endchar):
    s = ""
    c = " "
    c = fd.read(1)
    if c == "":
        return None
    while c != endchar:
        s = s + c
        c = fd.read(1)
    return s

################################################################################

# 引数処理: 定義
parser = optparse.OptionParser()
parser.add_option("-t", "--TEMPLATEFILE", dest="fn_temp")
parser.add_option("-c", "--CSVFILE", dest="fn_csv")

(options, args) = parser.parse_args()

# 引数処理: 内部変数へのimport
fn_temp = options.fn_temp
fn_csv =  options.fn_csv

is_readfromfile = False

if fn_temp == None:
    sys.exit()
if fn_csv == None:
    is_readfromfile = True

str_template = open(fn_temp).read()

fd = open(fn_csv, "r")

if __name__ == '__main__':
    # 頭の一行を読み込む
    line = read_until(fd, "\n")
    if line == None or line == "" or line[0] != "#":
        print "最初の一行は列の定義でなければなりません"
        sys.exit(0)
    (l_argc, l_argv) = line_proc_first(line)
    while line != None:
        line = read_until(fd, "\n")
        # EOF
        if line == None:
            break
        # skip COMMENTOUT/BLANK
        if line != "" and line[0] == "#":
            continue
        # Proc
        line_proc_replace(line, l_argc, l_argv)
