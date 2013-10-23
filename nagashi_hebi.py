#!/usr/bin/python
# -*- coding: utf-8 -*-

# にょろにょろ

"""
標準入力をぱらぱら(Cascadeのように)表示します。
-dをつけると毒蛇モードになります。
"""


import random
import sys, time
import optparse

def str2indexlist(stInput, inOffset = 0):
    """
    与えられた文字列の各文字について、['文字', '順序']を示す
    Listを返します。
    @inOffset: 最初の文字の順序

    実行例:
    >>> str2indexlist("hoge")
    [['h', 0], ['o', 1], ['g', 2], ['e', 3]]
    >>> str2indexlist("hoge", inOffset=1)
    [['h', 1], ['o', 2], ['g', 3], ['e', 4]]
    """
    return( map(lambda x,y: [x,y + inOffset], stInput, range(len(stInput))))


def cascade(stInput, dokuhebi=False, inDisplayInterval = 0.01):
    stDisplayBuffer = str2indexlist(stInput, inOffset = 1)
    random.shuffle(stDisplayBuffer)
    sys.stdout.write("\r")
    for x in stDisplayBuffer:
        (ch, cur) = x[0], x[1]
        if dokuhebi:
            sys.stdout.write("\033["+  str(cur) + "C" + "\033[3" + str(random.randint(1, 7)) + "m" +ch + "\033[" + str(cur+1) + "D")
        else:
            sys.stdout.write("\033["+  str(cur) + "C" + ch + "\033[" + str(cur+1) + "D")

        sys.stdout.flush()
        time.sleep(inDisplayInterval)
    sys.stdout.write("\n")

"""
オプションの処理
このプログラムは「毒蛇」オプションを持ちます。
これが指定されている場合、プログラムの出力はまるで毒蛇のようにカラフルになります
"""
parser = optparse.OptionParser()
parser.add_option("-d", "--DOKUHEBI", dest="f_dokuhebi", action="store_true" ,default=False)
(options, args) = parser.parse_args()
f_dokuhebi = options.f_dokuhebi

# STDINから「空白」が入力されるまで読み込みます
for line in iter(sys.stdin.readline, ""):
    cascade(line.rstrip(), f_dokuhebi)

