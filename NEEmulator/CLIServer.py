#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socketserver
import sys
import yaml
import re
from pprint import pprint

# テスト用YAML
TestServerYaml="""
local:
 host: "cisco1"
 ipaddrlo0: "192.168.255.1"

patterns:
  "logout":
    action: "exit"

  "hostname":
    action: "loop"
    res:
      - "{host}"

  "show version":
    res:
      - "{host}"
      - "end"

  "show bgp neighbor (?P<neighbor>[0-9.]+)":
    action: "writebuffer"    
    res:
      - ""
      - "{neighbor} idle"
      - "{neighbor} establish"

  "show (?P<foo>[0-9.]+) (?P<bar>[0-9.]+)":
    res:
      - "hello {foo}, {bar}"

"""

# debug用コード
pprint(yaml.load(TestServerYaml))

# デフォルト設定
HOST, PORT = "localhost", 10000

# SOREUSEADDR
socketserver.TCPServer.allow_reuse_address = True

class MyTCPHandler(socketserver.BaseRequestHandler):
    doexit = False
    def handle(self):
        """
        イベントハンドラ本体
        Connectしたセッションはこれに捕まるので、抜けるときはexitする
        :return:
        """
        self.curBuffer = oracle
        while True:
            self.data = self.request.recv(1024)
            if self.data == b'':
                print("EndSession")
                return
            print("TelnetRecv[{0}]: {1}".format( self.client_address[0], self.data))
            self.recvCmd(self.data)
            if self.doexit:
                print("session was deleted")
                return

    def write(self, s):
        if isinstance(s, bytes):
            s = s.decode(s)
        s = s + "\n"
        print("{0}".format(s))
        self.request.sendall(s.encode("utf-8"))

    def recvCmd(self, s):
        s = s.decode('utf-8')
        pprint(self.curBuffer)
        for p in self.curBuffer:
            m = re.search(p, s)
            if m:
                args = {}
                for x in re.finditer("\?P<([^>]*)>", p):
                    varname = x.groups()[0]
                    args[varname] = m.group(varname)
                #self.write("CMD: " + p)
                self.doCmd(p, self.curBuffer[p], args)
                return True
        self.write("command not found: " + s)
        return True
    
    def doCmd(self, key, p, args):
        action = p.get("action", "loop")
        if action == "exit":
            self.doexit = True
        elif action == "loop":
            liStr = p.get("res", [])
            curargs = val
            curargs.update(args)
            s = liStr[0].format(**curargs)
            self.write(s)
        elif action == "writebuffer":
            liStr = p.get("res", [])
            curargs = val
            curargs.update(args)
            s = liStr[0].format(**curargs)
            if len(liStr) > 1:
                p["res"] = liStr[1:]
            self.write(s)
            print(liStr)
            self.curBuffer[key] = p
            

        
if __name__ == "__main__":
  cfg = yaml.load(TestServerYaml)

  val = cfg.get("local", {})

  # コマンドを待ち受けるグローバルリスト
  oracle = cfg.get("patterns", {})

  # LISTENし、open後のハンドラをMyTCPHandlerに設定
  server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

  # while 1
  server.serve_forever()

