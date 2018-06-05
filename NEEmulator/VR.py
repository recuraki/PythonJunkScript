#!/usr/bin/python3
# -*- coding: utf-8 -*-

import yaml
import re
from pprint import pprint
from Logs import Log

# テスト用YAML
TestServerYaml="""
"""

class VR(object):
    doexit: bool = False
    BUFSIZ: int = 1024
    logseq: int = 0
    loglimit: int = 255
    isdebug: bool = False
    vrName: str = ""
    scenario: list = []
    log: Log = None

    def dp(self, log):
        if self.isdebug:
            pprint(log)

    def __init__(self, name: str="VR", debug: bool=False):
        """
        コンストラクタ
        :param name:
        :param debug:
        """
        self.isdebug = debug
        self.vrName = name
        self.log = Log()

    def recvLine(self, s):
        """
        新規入力受付時の処理。
        :param s:
        :return:
        """
        # self.recvCmd(self.data)
        # s = s.decode('utf-8')
        self.writeLog("input: ")
        # コマンドリストの正規表現を順次精査
        for p in self.curBuffer:
            m = re.search(p, s)
            # fetchできた場合
            if m:
                # パターン内に含まれる?P<name>を取得し、それらをargsに突っ込む
                args = {}
                for x in re.finditer("\?P<([^>]*)>", p):
                    varname = x.groups()[0]
                    args[varname] = m.group(varname)
                # 実際のコマンドを実行する
                # この際、上記で作成したargsを渡す
                self.doCmd(p, self.curBuffer[p], args)
                return True
        # パターンがいずれにもマッチしない場合の処理
        self.write("command not found: " + s)
        return True

    def doCmd(self, key, p, args):
        # 動作モードの確認
        action = p.get("action", "writebuffer")

        # exit: 即座にtelnet sessionを切断する
        if action == "exit":
            self.doexit = True

        # writebuffer バッファリストからデータを取得
        elif action == "writebuffer":
            # 応答リストをfetchする
            liStr = p.get("res", [])
            # curargsにlocal変数を入れる
            curargs = val
            # curargsに「コマンドから取得した応答」を更新する
            curargs.update(args)
            # 応答文字列内の{value}を適切に変換する
            s = liStr[0].format(**curargs)
            # リストに後続がある場合はshift(pop)する
            # 後続がない場合はそのまま＝最後の応答候補をそのまま返す
            if len(liStr) > 1:
                p["res"] = liStr[1:]
            self.curBuffer[key] = p

            # 応答を返す
            self.write(s)
            print(liStr)



if __name__ == "__main__":
    vr = VR(name="router1")

    cfg = yaml.load(TestServerYaml)

    val = cfg.get("local", {})

    # コマンドを待ち受けるグローバルリスト
    oracle = cfg.get("patterns", {})
