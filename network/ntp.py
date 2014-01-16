#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from scapy.all import *
from time import sleep
import sys

"""
Src Interfaceを指定したい場合は以下
conf.iface = "em0"

IPアドレスやMAC AddrをSpoofしたいときは以下のようにする
srcipaddr="192.168.0.1"
srcether="xx:xx:xx:xx:xx:xx"
dstether="yy:yy:yy:yy:yy:yy"
をいれて
      Ether(src=srcether,dst=dstether)/
      IP(src=srcipaddr,dst=dstipaddr)/
などとする

NTPのオプションに関しては
>>> scapy.NTP()
>>> NTP().show()
###[ NTP ]###
  leap      = nowarning
  version   = 3
  mode      = client
  stratum   = 2
  poll      = 10
  precision = 0
  delay     = 0.0
  dispersion= 0.0
  id        = 127.0.0.1
  ref       = 0.0
  orig      = --
  recv      = 0.0
  sent      = --
として見る
"""

dstipaddr="210.173.160.27"

print "NTP Pkt... "

ntp = (
      Ether()/
      IP(dst=dstipaddr)/
      UDP(sport=123,dport=123)/
      NTP(version=4, poll=4, stratum=0, delay=1.0, dispersion=1.0, id="0.0.0.0")
      )

print(ntp.show())
sendp(ntp, verbose=1) 
sendp(ntp, verbose=1) 
sendp(ntp, verbose=1) 
