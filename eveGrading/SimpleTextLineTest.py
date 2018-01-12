#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class SimpleTextLineTest():
    """
    指定された複数行テキストを改行でパースし、
    「含まれるべき文字列」のANDと
    「含まれてはいけない文字列」のORに一致するか判別する
    テストケースに対して以下のように返却される。
    例：(True, 'p', 'as200', None)
    (res, type, pattern, match)
    res: その文字列に対する結果
    type: p=positive-含まれるべき文字列, n=negative-含まれてはいけない文字列
    pattern: その評価文字列
    match: nの場合、マッチ「してしまった」文字列の部分範囲
    """
    text = ""
    lines = []
    positive_texts = []
    negative_texts = []
    result = []
    f_pass = False
    debug = False

    def __init__(self, text, Positive, Negative, argvFormat = {}, debug = False):
        """

        :param text: 対象となる複数文字列(0x0dでsplitされる)
        :param Positive: 含まれるべき文字列のリスト
        :param Negative: 含まれてはならない文字列のリスト
        :param debug: デバッグメッセージの有無(default: False)
        :param argvFormat: {pattern}を置換するpattern: strのリスト
        """
        self.text = text
        self.lines =  text.split("\n")
        self.positive_texts = Positive
        self.negative_texts = Negative
        self.argv = argvFormat
        self.debug = debug
        self.execute()

    def execute(self):
        """
        試験結果の表示
        この試験の実施後、raw_resultにて詳細の結果を得られる
        :return: True, False
        """
        self.result = []
        self.f_pass = False
        r1 = self.exec_Positive()
        r2 = self.exec_Negative()
        self.f_pass = r1 and r2
        return self.f_pass

    def dp(self, s):
        if self.debug:
            print(s)

    def exec_Positive(self):
        """
        含まれるべき文字列の評価関数
        :return:
        """
        f_matchall = True
        # positive[]に対してfor
        for pat in self.positive_texts:
            pat = pat.format(**self.argv)
            f_found = False
            # 対象文字列すべてを操作
            for l in self.lines:
                # 見つけたら抜ける
                if re.search(pat, l):
                    f_found = True
                    break
            # もし見つけずに最後まで来てしまったら
            if f_found == False:
                self.result.append((False, "p", pat, None))
                f_matchall = False
                # 評価を失敗とする
                break
            self.result.append((True, "p", pat, None))
        return f_matchall

    def exec_Negative(self):
        f_noall = True
        # negative[]に対してfor
        for pat in self.negative_texts:
            pat = pat.format(**self.argv)
            f_notfound = True
            mstr = ""
            # 対象文字列すべてを操作
            for l in self.lines:
                res = re.search(pat, l)
                # 「見つかった」場合だけ抜ける＝失敗
                if res:
                    f_notfound = False
                    mstr = l.strip()
                    break
            # もしも、見つかってしまったのなら
            if f_notfound == False:
                self.result.append((False, "n", pat, mstr))
                f_noall = False
                # 失敗を返す
                break
            self.result.append((True, "n", pat, None))
        return f_noall

    def is_pass(self):
        return self.f_pass

    def raw_result(self):
        # この結果は、execute後に詳細な情報を得るために用いられる
        return self.result

str="""
neighbor as100 192.168.100.1
neighbor as200 192.168.100.2
neighbor as200 192.168.100.3
neighbor as300 192.168.100.4
"""


if __name__ == "__main__":
    p = ["as200", "as300"]
    n = ["as100"]
    print (SimpleTextLineTest(str, p, n, debug=True).raw_result())
