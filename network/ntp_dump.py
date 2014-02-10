#!/opt/local/bin/python2.7
# -*- coding: utf-8 -*-

from scapy.all import *
from time import sleep
import sys
import time
import datetime

while True: 
  time.sleep(1)
  stime = time.time()
  pkt = sniff(iface="en0", filter="port 123 ", count=1)
  etime = time.time()
  if pkt == []:
    print("T/O")
  else:
    npkt = pkt[0]["NTP"]
    print npkt.show()
    print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S") + "," + str(npkt.precision) + "," + str(npkt.delay) + "," + str(npkt.dispersion) + "," + str(etime - stime))
