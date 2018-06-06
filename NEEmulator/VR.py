#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pprint import pprint
from Logs import Log
from Scenario import Scenario

class VR(object):
    doexit: bool = False
    BUFSIZ: int = 1024
    logseq: int = 0
    loglimit: int = 255
    isdebug: bool = False
    vrName: str = ""
    scenario: Scenario = None
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
        self.scenario = Scenario(debug=True)

    def loadscenario(self, data):
        self.dp("VR loadscenario() ")
        self.scenario.read(data)

    def send(self, s):
        """
        新規入力受付時の処理。
        :param s:
        :return:
        """
        self.dp("VR.send(): vrName[{0}] recv: {1}".format(self.vrName, s))
        ret = self.scenario.send(s)
        if ret.get("match", False):
            print("match")
            responseStr = "match"
        else:
            responseStr = False
        return responseStr

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
