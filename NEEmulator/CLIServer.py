#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socketserver
import sys
import yaml
import re
from pprint import pprint

TestServerYaml="""
local:
 host: "cisco1"
 ipaddrlo0: "192.168.255.1"

patterns:
  "logout":
    action: "exit"
  "hostname":
    res:
     -
       - "%{host}s"
  "show version":
    res:
     -
       - "%{host}s"
"""

pprint(yaml.load(TestServerYaml))
HOST, PORT = "localhost", 10000

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.curBuffer = oracle
        while True:
            self.data = self.request.recv(1024)
            if self.data == b'':
                print("EndSession")
                return
            print("TelnetRecv[{0}]: {1}".format( self.client_address[0], self.data))
            self.recvCmd(self.data)

    def write(self, s):
        if isinstance(s, bytes):
            s = s.decode(s)
        print("Write : {0}".format(s))
        self.request.sendall(s.encode("utf-8"))

    def recvCmd(self, s):
        s = s.decode('utf-8')
        pprint(self.curBuffer)
        for p in self.curBuffer:
            m = re.search(p, s)
            if m:
                self.write("CMD: " + p)
                self.doCmd(self.curBuffer[p])
                return True
        self.write("command not found: " + s)
        return False
    def doCmd(self, p):
        pass
        

        


if __name__ == "__main__":
  cfg = yaml.load(TestServerYaml)
  val = cfg.get("local", {})
  # コマンドを待ち受ける全能のOracle
  oracle = cfg.get("patterns", {})
  pprint(val)

  # SOREUSEADDRしてLISTEN
  socketserver.TCPServer.allow_reuse_address = True
  server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
  # while 1
  server.serve_forever()

