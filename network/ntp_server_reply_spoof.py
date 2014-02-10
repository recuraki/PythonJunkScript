#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from scapy.all import *
from time import sleep
import time
import datetime
import sys

dstipaddr="10.1.1.1"


def send_NTP():
  inCurTime = int(time.time()) + 2208988800 + 1
  inBigCurTime = inCurTime 
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

while True:
  time.sleep(0.1)
  pkt = sniff(filter="port 123", count=1, timeout=1)
  if pkt == []:
    print("T/O")
  else:
    npkt = pkt[0]["NTP"]
    print npkt.underlayer.mode
    if npkt.mode == 3:
      print npkt.sent
