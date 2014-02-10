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

dstipaddr="192.168.0.1"

print "NTP Pkt... "

ntp = (
      Ether()/
      IP(dst=dstipaddr)/
      UDP(sport=123,dport=123)/
      NTP(version=4, mode="server", poll=4L, stratum=1L, delay=1.0, dispersion=1.0, id="8.8.8.8", precision=235L, ref=time.time())
      )

print(ntp["NTP"].show())
#sendp(ntp, verbose=1) 
