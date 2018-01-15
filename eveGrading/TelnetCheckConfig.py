#!env python3.5
# -*- coding: utf-8 -*-

from pprint import pprint
import sys
import time
from telnetlib import Telnet
from SimpleTextLineTest import  SimpleTextLineTest
import yaml

class TelnetCheckConfig():
    """
    当該ホストへのtelnetを行い、指定した文字列を打って、戻り値を評価するライブラリ
    """
    expectuntil = ""
    debug = False
    promptName = ""
    def __init__(self, debug = False):
        self.debug = debug
        pass

    def dp(self, d):
        if self.debug == True:
            print(d)

    def connect(self, host, port, expectuntil, enablePass = "cisco"):
        """
        Ciscoノードへの接続
        :param host:
        :param port:
        :param expectuntil:
        :param enablePass:
        :return:
        """
        # 待ち受けよう文字列の準備
        self.promptName = expectuntil
        self.expectuntil = expectuntil.encode("ascii")
        prUsermode = self.expectuntil + ">".encode("ascii")
        prExecmode = self.expectuntil + "#".encode("ascii")
        prConfigmode = self.expectuntil + "\(".encode("ascii")

        #telnetする
        self.t = Telnet(host, port=port)
        # login直後のやさしさ(telnetからの応答を一つよみこむ
        (index, reobj, res) = self.t.expect([self.expectuntil], timeout = 1)
        if index == -1:
            return -1

        # 0x0aは最悪、show runとかで--more--してても抜けられる
        self.t.write(b"\r\n")
        # \r\nを送った場合、1回ダミーの設定のexpectを入れる
        (index, reobj, res) = self.t.expect([self.expectuntil])
        # 今のモードを識別する
        (index, reobj, res) = self.t.expect([prExecmode, prUsermode, prConfigmode], timeout=1)
        # enableの場合何もしない
        if index == 0:
            pass
        # loginならenableする。パスワードが必要ならログインする
        elif index == 1:
            self.t.write(b"enable\n")
            (index, reobj, res) = self.t.expect([prExecmode, b"Password"])
            if index == 1:
                self.write(enablePass)
        # configモードは抜ける
        elif index == 2:
            self.write("end")
        # 余計なログをひっかけないようにする
        self.write("ter len 0")
        self.write("conf t", rough=True)
        self.write("no logg con", rough=True)
        self.write("end")

    def write(self, cmd, rough= False):
        """
        :param cmd:
        :param rough: Trueならホスト名だけで次に行く.Falseならenableモードか確認する
        :return:
        """
        self.dp("send: {0}".format(cmd))
        self.t.write(cmd.encode("ascii") + b"\n")
        if not rough:
            waitWord = self.expectuntil + "#".encode("ascii")
        else:
            waitWord = self.expectuntil
        (index, reobj, res) = self.t.expect([waitWord])
        #self.dp("recv: {0}".format(res.decode("utf-8")))

    def do_singletest(self, cmd, p = [], n = []):
        """
        :param cmd: これを実施する
        :param p: 含まれるべき文字列
        :param n: 含まれてはならない文字列
        :return: 結果true or false
        """
        # 指定文字列の実行
        self.dp("send: {0}".format(cmd))
        self.t.write(cmd.encode("ascii") + b"\n")
        (index, reobj, res) = self.t.expect([self.expectuntil])

        # 応答を評価する
        res = res.decode("utf-8")
        stlt = SimpleTextLineTest(res, p, n, debug=True)
        is_pass = stlt.is_pass()
        # 結果の詳細を格納
        result = stlt.raw_result()
        stlt = None
        # 結果をターミナルに書く
        resultstr = self.result2str(result)
        for l in resultstr:
            self.write("!" + l)
        return is_pass

    def result2str(self, result):
        """
        ターミナルに出力するようの
        :param result:
        :return:
        """
        res = []
        for fp, type, pat, negline in result:
            l = ""
            l = l + "[OK]:" if fp else "[ERROR]:"
            if type == "p":
                l = l + "INCLUDE [{0}]".format(pat)
            elif type == "n":
                l = l + "NOT-INCLUDE [{0}]".format(pat)
            res.append(l)
        return res

    def disconnect(self):
        self.write("ter len 24")
        self.write("conf t", rough=True)
        self.write("logg con", rough=True)
        self.write("end")
        self.t.close()

    def test(self, diTests):
        res = []
        ipaddr = diTests.get("ipaddr", "127.0.0.1")
        port = diTests.get("port", "23")
        hostname = diTests.get("hostname", "localhost")
        prompt = diTests.get("prompt", hostname)
        self.connect(ipaddr, port, prompt)
        final_pass = True
        for t in diTests.get("tests", []):
            name = t.get("name", "NONAME")
            self.write("!!!!!!! BEGIN Test: {0}".format(name))
            cmd = t.get("cmd", [])
            p = t.get("include", [])
            n = t.get("notinclude", [])
            is_pass = self.do_singletest(cmd, p, n)
            final_pass = final_pass and is_pass
            self.write("!!!!!!! END")
            self.write("")
            res.append((name, is_pass))
        return (self.promptName, final_pass, res)

    def showRun(self, ipaddr, port, prompt, timeout = 5):
        r = self.connect(ipaddr, port, prompt)
        if r == -1:
            return (-1, None, "")
        self.t.write("show run |  exclude Last conf|Current c|Building".encode("ascii") + b"\n")
        (index, reobj, res) = self.t.expect([self.expectuntil + "#".encode("ascii")], timeout = 3)
        pprint(res)
        # timeoutの時は、reobj = None, index = -1で返ります
        return(index, reobj, res.decode("utf-8"))

    def writeResult(self, result):
            """
            最終結果のコンソールへの表示
            :param result:
            :return:
            """
            self.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            finalResult = True
            for name, is_pass in result:
                s = "PASS" if is_pass else "FAIL"
                finalResult = finalResult and is_pass
                self.write("! [{0}]: {1}".format(s, name))
            self.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.write("! FINAL RESULT [{0}]".format("PASS" if finalResult else "FAIL"))

    def writeResult2stdout(self, result):
        """
        最終結果のターミナルへの表示
        :param result:
        :return:
        """
        print("")
        finalResult = True
        for name, is_pass in result:
            finalResult = finalResult and is_pass
        print("##### {0} [{1}]".format(self.promptName, "OK" if finalResult else "FAIL"))
        for name, is_pass in result:
            s = "PASS" if is_pass else "FAIL"
            finalResult = finalResult and is_pass
            print("  [{0}]: {1}".format(s, name))

