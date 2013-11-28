#!env python
# -*- coding: utf-8 -*-

import sys

diPermutation = {}
diPermutation["a"] = ["a", "A", "@", "a"]
diPermutation["b"] = ["b", "B"]
diPermutation["c"] = ["c", "C"]
diPermutation["d"] = ["d", "D"]
diPermutation["e"] = ["e", "E", "3"]
diPermutation["f"] = ["f", "F"]
diPermutation["g"] = ["g", "G", "9"]
diPermutation["h"] = ["h", "H"]
diPermutation["k"] = ["k", "K"]
diPermutation["i"] = ["i", "I", "1", "!", "|"]
diPermutation["j"] = ["j", "J"]
diPermutation["k"] = ["k", "K"]
diPermutation["l"] = ["l", "L", "1", "7", "!", "|"]
diPermutation["m"] = ["m", "M"]
diPermutation["n"] = ["n", "N"]
diPermutation["o"] = ["o", "O", "0"]
diPermutation["p"] = ["p", "P"]
diPermutation["q"] = ["q", "Q"]
diPermutation["r"] = ["r", "R"]
diPermutation["s"] = ["s", "S", "5", "$"]
diPermutation["t"] = ["t", "T", "7", "1", "+"]
diPermutation["u"] = ["u", "U", "v", "V"]
diPermutation["v"] = ["v", "V", "u", "U"]
diPermutation["w"] = ["w", "W", "vv"]
diPermutation["x"] = ["x", "X"]
diPermutation["y"] = ["y", "Y"]
diPermutation["z"] = ["z", "Z", "2"]

liKeyLetter = []
# diPermutationを捜査中はdiPermutationでforが回せないので、一時変数を作ります
for chLetter in diPermutation:
    liKeyLetter.append(chLetter)

"""
索引の重複削除
diPermutation["a"] = ["a", "A", "@", "a"]
を
diPermutation["a"] = ["a", "A", "@"]
にする
"""
for chLetter in liKeyLetter:
    liCur = diPermutation[chLetter]
    for chCur in liCur:
        for inLoop in range(liCur.count(chCur) - 1):
            liCur.remove(chCur)

"""
索引の拡張(索引の文字の索引を適正にする)
たとえば
diPermutation["o"] = ["o", "O", "0"]
diPermutation["0"] = ["O", "0"]
というリストを
diPermutation["o"] = ["o", "O", "0"]
diPermutation["O"] = ["O", "o", "0"]
diPermutation["0"] = ["O", "0", "o"]
というようにします
"""
for chLetter in liKeyLetter:
    for chCur in diPermutation[chLetter]:
        for chCurChild in diPermutation[chLetter]:
            if not chCur in diPermutation:
                diPermutation[chCur] = [chCur]
            if not chCurChild in diPermutation[chCur]:
                diPermutation[chCur].append(chCurChild)

def MakeSubspecies(stWord, inIndex = 0):

    inLenWord = len(stWord)

    # 文字の最後に到達した場合、この時の文字列を返す
    if inIndex >= inLenWord:
        print stWord
        return

    # 現在の文字を得る
    chCurrent = stWord[inIndex]

    """
    文字に対応する置換文字の表を得る
    対応する表が存在しない場合、その文字だけのリストを返す。
    例: a => ['a', 'A', '@']
        1 => ['1'](存在しなければ)
    """
    liSuggestChar = diPermutation.get(chCurrent, [chCurrent])

    # これらの候補文字列を作っていく
    for chCurSuggest in liSuggestChar:
        stCutSuggest =  stWord[:inIndex] + chCurSuggest + stWord[inIndex + 1:]
        MakeSubspecies(stCutSuggest, inIndex + 1)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        MakeSubspecies(sys.argv[1], 0)
