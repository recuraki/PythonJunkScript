#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from scapy.all import *
from time import sleep
import sys
import time
import datetime

while True: 
  time.sleep(1)
  stime = time.time()
  pkt = sniff(iface="em0", filter="port 123 ", count=2)
  etime = time.time()
  if pkt == []:
    print("T/O")
  else:
    npkt = pkt[0]["NTP"]
    print npkt.show()
    print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S") + "," + str(npkt.precision) + "," + str(npkt.delay) + "," + str(npkt.dispersion) + "," + str(etime - stime))
    npkt = pkt[1]["NTP"]
    print npkt.show()
    print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S") + "," + str(npkt.precision) + "," + str(npkt.delay) + "," + str(npkt.dispersion) + "," + str(etime - stime))
