#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from scapy.all import *
from time import sleep
import sys
import time
import datetime

if (len(sys.argv) != 2):
  quit()

dstipaddr = sys.argv[1]

ntp = (
      Ether()/
      IP(dst=dstipaddr)/
      UDP(sport=123,dport=123)/
      NTP(version=4, poll=4, stratum=0, delay=1.0, dispersion=1.0, id="0.0.0.0")
      )


while True: 
  time.sleep(1)
  stime = time.time()
  sendp(ntp, verbose=0) 
  pkt = sniff(filter="port 123 and host " + dstipaddr, count=1, timeout=1)
  etime = time.time()
  if pkt == []:
    print("T/O")
  else:
    npkt = pkt[0]["NTP"]
    print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S") + "," + str(npkt.precision) + "," + str(npkt.delay) + "," + str(npkt.dispersion) + "," + str(etime - stime))
