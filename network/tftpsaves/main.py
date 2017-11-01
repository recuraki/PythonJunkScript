#!/usr/bin/python3.5
# -*- coding: utf-8 -*-


# pexpectはちゃんと非同期処理に対応していません。
# 並列において以下のパッチが必要
# https://github.com/pexpect/pexpect/pull/376/files#r78765769

# そもそも、コルーチン系を使うにはPython3.5以上が必要になります。
# Ubuntuの場合、以下のようにすること
#
# sudo add-apt-repository ppa:fkrull/deadsnakes
# sudo apt-get update
# sudo apt-get install python3.5
# wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
# sudo python3.5 /tmp/get-pip.py
# sudo pip3.5 install pexpect
# sudo pip3.5 install PyYAML
# sudo pip3.5 install requests
#

import asyncio
import time
import pexpect
import sys
import yaml
import requests
import json
from optparse import OptionParser

# サンプル用のテストConfig
sample_yaml="""
global:
 tftpserver: "192.168.196.99"
 slackmode: "error"
 slackurl: "https://hooks.slack.com/services/xxx/xxx/xxx"
 slackchannel: "#bot-notification"
 slackusername: "tftpsan"
nodes:
 - name: "crs1k-1"
   type: "iosxe"
   spawn: "telnet 192.168.196.100"
   loginuser: "name"
   loginpass: "pass"
 - name: "crs1k-1-clone"
   type: "iosxe"
   spawn: "telnet 192.168.196.100"
   loginuser: "name"
   loginpass: "pass"
"""

##### 例外 #######
class AuthError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)


##### IOS-XE向けモジュール #######
class CiscoIOSXE:
    p = None
    name = ""
    is_enable = False
    loginuser = None
    loginpass = None
    enablepass = None
    def __init__(self, d):
        self.p = pexpect.spawn(d["spawn"], encoding="utf-8")
        self.p.logfile = sys.stdout
        self.name = d["name"]
        self.loginuser = d.get("loginuser", "")
        self.loginpass = d.get("loginpass", "")
        self.enablepass = d.get("loginpass", "")
        self.enablepass = d.get("enablepass", self.enablepass)
        self.msg("INIT")

    # モジュール内ではnoticeをmsg()にて送る。非同期処理のため、頭につけるのを
    # setPromptで行う
    def setPrompt(self, prompt):
        self.msg("set PROMPT: {0}".format(prompt))
        self.prompt = prompt

    def msg(self, msg):
        print("[{0}]: {1}".format(self.name, msg))

　　# 非同期 login
    @asyncio.coroutine
    def login(self):
        try:
            yield from self.p.expect("name: ", async=True)
        except pexpect.exceptions.TIMEOUT as e:
            raise e

        self.p.sendline(self.loginuser)

        yield from self.p.expect("word: ", async=True)
        self.p.sendline(self.loginpass)

        i = yield from self.p.expect([r">", r"#", r"(Authentication failed|Login invalid)",],
                                 async=True)
        if i == 0:
            self.setPrompt(self.p.before.split("\n")[-1])
        elif i == 1:
            self.setPrompt(self.p.before.split("\n")[-1])
            self.is_enable = True
        elif i == 2:
            raise AuthError("login")

    # enableに入る
    @asyncio.coroutine
    def enable(self):
        self.msg("enable P:")
        if self.is_enable:
            return
        self.p.sendline("enable")
        i = yield from self.p.expect([self.prompt + "#", r"word: "], async = True)
        if i == 0:
            self.msg("already enable")
            self.is_enable = True
            return
        self.p.sendline(self.enablepass)
        i = yield from self.p.expect([self.prompt + "#", r"Access denied"], async = True)
        if i == 1:
            raise AuthError("enable")
        self.msg("enable ok")

    # [コマンド処理]
    # @path: tftp://..../... の形式で入れる
    @asyncio.coroutine
    def tftpbackup(self, path):
        # ログイン
        try:
            yield from self.login()
        except AuthError as e: # 認証拒否
            return({"name": self.name, "status": "AuthError: " + e.value , "res": "", })
        except pexpect.exceptions.EOF as e:
            return({"name": self.name, "status": "Timeout"  , "res": "", })
        except pexpect.exceptions.TIMEOUT as e:
            return({"name": self.name, "status": "Timeout"  , "res": "", })

        # enable
        try:
            yield from self.enable()
        except AuthError as e: # 拒否
            return({"name": self.name, "status": "AuthError: " + e.value , "res": "", })
        except pexpect.exceptions.EOF as e:
            return({"name": self.name, "status": "Timeout"  , "res": "", })

        # 同期: コマンドの実行
        self.p.sendline("copy running-config {0}".format(path))

        # HostName?をまつ -> そのままエンター
        try:
            yield from self.p.expect("(remote host|Host name)", async = True)
        except pexpect.exceptions.EOF as e:
            return({"name": self.name, "status": "Timeout"  , "res": "", })
        self.p.sendline("")

        # FileName?を待つ -> そのままエンター
        try:
            yield from self.p.expect("(filename|file name)", async = True)
        except pexpect.exceptions.EOF as e:
            return({"name": self.name, "status": "Timeout"  , "res": "", })
        self.p.sendline("")

        # 実施結果の確認
        # 0: プロンプトが帰ってきた＝成功
        # 1: Permission denied
        # 2: タイムアウト
        try:
            i = yield from self.p.expect([self.prompt + "#", r"Permission denied", "Timed out"], async = True, timeout = 40)
        except pexpect.exceptions.EOF as e:
            return({"name": self.name, "status": "Timeout"  , "res": "", })
        if i == 1:
            return({"name": self.name, "status": "TFTPServer: Permission denied"  , "res": "", })
        elif i == 2:
            return({"name": self.name, "status": "TFTPServer: Timeout"  , "res": "", })

        # 後処理
        self.p.sendline("logout")

        # 結果の記録
        return({"name": self.name, "status": "ok", "res": "", })


# これ、registTaskとした方がいいかも
def readYaml(dat, userdata):
    cors = []
    # Global Configurationの読み込み
    g = dat["global"]
    # 各ノード情報を上書き
    for e in dat["nodes"]:
        # グローバル設定を優先して、情報を書き込み
        d = g.copy()
        d.update(e)
        # ユーザ入力情報を差し込み
        d.update(u)
        # ノードごとの分岐
        if d["type"] == "iosxe":
            o = CiscoIOSXE(d)
        else:
            continue
        path = "tftp://" + d["tftpserver"] + "/"
        path = path + d["destPrefix"] + d["name"] + d["destSuffix"]
        # ここで、こっそり、taskを積み込んでいる
        cors.append(o.tftpbackup(path))
    return(cors)

# Slack通知のメッセージ作成
# slackmode = all だったら実施のたびにログを出す
# slackmode = error の時はエラーだけしか返さない
def doNotificationSlackCreatemsg(dat, res):
    text = ""
    if dat["global"]["slackmode"] == "all":
         for r in res:
              if r["status"] == "ok":
                   text += "{0}:OK".format(r["name"]) + "\n"
              else:
                   text += "{0}:Error {1}".format(r["name"], r["status"]) + "\n"
    if dat["global"]["slackmode"] == "error":
         for r in res:
              if r["status"] == "ok":
                   pass
              else:
                   text += "{0}:Error {1}".format(r["name"], r["status"]) + "\n"
    return(text)

# Slack通知を行う
def doNotificationSlack(dat, res):
    d = {
     "text": "DEFAULT",
     "username": 'tftpsave',
     "icon_emoji":':grin:',
     "channel":'#general',
    }
    if not "slackurl" in dat["global"]:
         print("ERROR: no slackutl")
         return
    d["channel"] = dat["global"].get("slackchannel", '#general')
    d["username"] = dat["global"].get("slackusername", 'tftpsave')
    url = dat["global"]["slackurl"]
    text = doNotificationSlackCreatemsg(dat, res)
    if text == "":
         print("aaa")
         return
    d["text"] = "TFTP PROCESS>>\n" + text
    r = requests.post(url, data=json.dumps(d))



# 実施結果の通知を行う(今はslackだけ)
def doNotification(dat, res):
     if dat["global"].get("slackmode", "") in ("all", "error"):
          doNotificationSlack(dat, res)

# 変数のパース
def argParser():
     arg = {}
     parser = OptionParser()
     parser.add_option("-c", "--CONFIG",
                       dest="fn_config", default=None)
     parser.add_option("-p", "--PREFIX",
                       dest="destPrefix", default="")
     parser.add_option("-s", "--SUFFIX",
                       dest="destSuffix", default="")
     (options, args) = parser.parse_args()
     arg["fn_config"] = options.fn_config
     arg["destPrefix"] = options.destPrefix
     arg["destSuffix"] = options.destSuffix
     return arg


fn_config = None

dat = yaml.load(sample_yaml)
if __name__ == "__main__":
    u = argParser()

    if u["fn_config"]:
        fr = open(u["fn_config"], "r")
        y = fr.read()
        dat = yaml.load(y)

    # Taskを登録する
    # corsには[func, func, func...]が積まれている
    cors = readYaml(dat, u)
    loop = asyncio.get_event_loop()
    # ここで非同期タスクを同期にする(runして、全ての完了を待つ)
    res = loop.run_until_complete(asyncio.gather(*cors))

    print("")
    for r in res:
         if r["status"] == "ok":
              print("{0}: DONE".format(r["name"]))
         else:
              print("{0}: Error {1}".format(r["name"], r["status"]))

    doNotification(dat, res)
