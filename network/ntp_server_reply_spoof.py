#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from scapy.all import *
from time import sleep
import time
import datetime
import sys

"""
###[ NTP ]###
  leap      = nowarning
  version   = 4L
  mode      = server
  stratum   = 1L
  poll      = 4L
  precision = 235L
  delay     = 0.0
  dispersion= 0.0020751953125
  id        = 1.1.1.1
  ref       = Mon, 10 Feb 2014 07:21:50 +0000
  orig      = Mon, 10 Feb 2014 07:22:01 +0000
  recv      = Mon, 10 Feb 2014 07:22:00 +0000
  sent      = Mon, 10 Feb 2014 07:22:00 +0000
None
"""

#conf.iface = "em0"
dstipaddr="10.1.1.1"

inCurTime = int(time.time()) + 2208988800 + 1
print "%x" % inCurTime
inBigCurTime = int()
inBigCurTime += (inCurTime & 0x000000ff) << 8 
inBigCurTime += (inCurTime & 0x0000ff00) >> 8 
inBigCurTime += (inCurTime & 0x00ff0000) << 8
inBigCurTime += (inCurTime & 0xff000000) >> 8
inBigCurTime = inBigCurTime << 32
#inBigCurTime = inBigCurTime << 16
inBigCurTime = inCurTime 
print "%x" % inBigCurTime
ntp = (
      Ether(src="11:11:11:11:11:11", dst="22:22:22:22:22:22")/
      IP(src="1.1.1.1", dst=dstipaddr)/
      UDP(sport=123,dport=123)/
      NTP(
        version=4,
        mode="server",
        poll=long(6),
        stratum=long(1),
        delay=0.0,
        dispersion=0.00248718261719,
        id="8.8.8.8", 
        precision=235L,
        ref = inBigCurTime,
        orig = inBigCurTime,
        recv=inBigCurTime,
        sent=inBigCurTime,
       )
      )

print(ntp["NTP"].show())
sendp(ntp, verbose=1, iface="em0") 
