#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socketserver
import sys
import yaml
import re
from pprint import pprint

# テスト用YAML
TestServerYaml="""
"""

class VR(object):
    doexit = False
    BUFSIZ = 1024

    def handle(self):
        """
        イベントハンドラ本体
        Connectしたセッションはこれに捕まるので、抜けるときはexitする
        :return:
        """
        # 応答リストの定義
        self.curBuffer = oracle

        while True:
            # 1024文字受け取る
            self.data = self.request.recv(self.BUFSIZ)
            # セッションが切られた時の処理
            if self.data == b'':
                print("EndSession")
                return
            # 受け取った文字列の表示
            print("TelnetRecv[{0}]: {1}".format( self.client_address[0], self.data))

            # 受け取った文字列の処理
            self.recvCmd(self.data)

            # 処理の結果、終了が明示された時の処理
            if self.doexit:
                print("session was deleted")
                return

    def write(self, s):
        # 文字列がバイナリの場合、一度文字列に変換
        if isinstance(s, bytes):
            s = s.decode(s)
        s = s + "\n"
        # console と 相手に応答を返す
        print("{0}".format(s))
        self.request.sendall(s.encode("utf-8"))

    def recvCmd(self, s):
        """
        コマンド受信時の処理
        :param s:
        :return:
        """
        s = s.decode('utf-8')
        pprint(self.curBuffer)
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
  cfg = yaml.load(TestServerYaml)

  val = cfg.get("local", {})

  # コマンドを待ち受けるグローバルリスト
  oracle = cfg.get("patterns", {})

  # LISTENし、open後のハンドラをMyTCPHandlerに設定
  server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

  # while 1
  server.serve_forever()

