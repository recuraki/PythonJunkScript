#!/usr/bin/python3.5

#If your ubuntu don't have python35 pkg,
# sudo add-apt-repository ppa:fkrull/deadsnakes
# sudo apt-get update
# sudo apt-get install python3.5
# wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
# sudo python3.5 /tmp/get-pip.py
# pip3.5 install pexpect

import asyncio
import time
import pexpect
import sys

class CiscoIOSXE:
    p = None
    name = ""
    is_enable = False
    loginuser = None
    loginpass = None
    enablepass = None
    def __init__(self, spawn, name = "", loginuser =None,
                 loginpass =None, enablepass=None):
        self.p = pexpect.spawn(spawn, encoding="utf-8")
        self.p.logfile = sys.stdout
        self.name = name
        self.loginuser = loginuser
        self.loginpass = loginpass
        self.enablepass = loginpass
        if enablepass != None:
            self.enablepass = enablepass
        self.msg("INIT")

    @asyncio.coroutine
    def login(self):
        yield from self.p.expect("name", async=True)
        self.p.sendline(self.loginuser)
        yield from self.p.expect("word", async=True)
        self.p.sendline(self.loginpass)
        i = yield from self.p.expect([r">", r"#", r"Authentication failed"],
                                 async=True)
        if i == 0:
            self.setPrompt(self.p.before.split("\n")[-1])
        elif i == 1:
            self.setPrompt(self.p.before.split("\n")[-1])
            self.is_enable = True
        elif i == 2:
            return "AuthError"

    @asyncio.coroutine
    def enable(self):
        self.msg("enable P:")
        if self.is_enable:
            return
        self.p.sendline("enable")
        i = yield from self.p.expect(["#", r"word"], async = True)
        if i == 0:
            self.msg("already enable")
            self.is_enable = True
            return
        self.p.sendline(self.enablepass)
        yield from self.p.expect(str(self.prompt + "#"), async = True)
        self.msg("enable ok")

    def setPrompt(self, prompt):
        self.msg("set PROMPT: {0}".format(prompt))
        self.prompt = prompt

    def msg(self, msg):
        print("[{0}]: {1}".format(self.name, msg))

    @asyncio.coroutine
    def tftpbackup(self, path):
        yield from self.login()
        yield from self.enable()
        self.p.sendline("copy running-config {0}".format(path))
        yield from self.p.expect("remote host", async = True)
        self.p.sendline("")
        yield from self.p.expect("filename", async = True)
        self.p.sendline("")
        yield from self.p.expect(self.prompt + "#", async = True)
        self.p.sendline("logout")


@asyncio.coroutine
def func():
    cors = [
        c.tftpbackup("tftp://192.168.196.99/temp"),
        c2.tftpbackup("tftp://192.168.196.99/temp"),
    ]
    yield from asyncio.wait(cors)

c = CiscoIOSXE("telnet 192.168.196.100", name="csr1", loginuser = "name", loginpass = "pass")
c2 = CiscoIOSXE("telnet 192.168.196.100", name="csr1", loginuser = "name", loginpass = "pass")
c.login()
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())
    


