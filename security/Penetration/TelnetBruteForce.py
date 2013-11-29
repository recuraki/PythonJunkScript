#!env python
# -*- coding: utf-8 -*-

import pexpect

class TelnetBruteForce():
    timeout = 5
    inPort = 0
    f_debug = False

    def __init__(self, f_debug = False):
        print "hoge"
        self.inPort = 23
        self.f_debug = f_debug
        
    def set_keyword_user(self, stInput):
        """
        ユーザ名を入力するキーワードを指定します
        例: Login: 
        """
        self.KWUser = stInput

    def set_keyword_pass(self, stInput):
        """
        パスワードを入力するキーワードを指定します
        例: Input Password:
        """
        self.KWPass = stInput

    def set_keyword_fail(self, stInput):
        """
        ログインに失敗した際のキーワードを指定します
        """
        self.KWFail = stInput

    def set_host_name(self, stHostname):
        """
        ログイン対象のホストを指定します
        """
        self.stHostname = stHostname

    def set_host_port(self, inPort):
        """
        telnetに用いるポート番号を指定します
        """
        self.inPort = inPort

    def dprint(self, stMessage):
        if self.f_debug:
            print(stMessage),

    def dprint_telnet(self, c):
        self.dprint(c.before + c.buffer + c.after)

    def login(self, stUsername, stPassword, inFailTimeout = 999):
        if inFailTimeout == 999:
            inFailTimeout = self.timout
        stCmd = "telnet " + self.stHostname + " " + str(self.inPort)
        self.dprint("Exec: " + stCmd)
        c = pexpect.spawn(command= stCmd, timeout=self.timeout)
        c.expect(self.KWUser)
        self.dprint_telnet(c)
        c.send(stUsername)
        c.send("\r")
        c.expect(self.KWPass)
        self.dprint_telnet(c)
        c.send(stPassword)
        c.send("\r")
        try:
            c.expect(self.KWFail, timeout = inFailTimeout)
        except pexpect.TIMEOUT:
            self.dprint(c.before)
            c.close()
            return True
        c.close()
        return False

def setNode_Brocade(t):
    t.set_keyword_user("Login Name:")
    t.set_keyword_pass("Password:")
    t.set_keyword_fail("User login failure")
    
def setNode_Juniper(t):
    t.set_keyword_user("login: ")
    t.set_keyword_pass("Password:")
    t.set_keyword_fail("Login incorrect")
    
