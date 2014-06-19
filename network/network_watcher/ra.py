#!/usr/bin/python
# -*- coding: utf-8 -*-

from scapy.all import *
from time import sleep
import sys
import time
import datetime
import random
import threading

class RAReciver(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

  def handle(handle, pkt):
    if ICMPv6ND_RA in pkt:
      server_mac = pkt.src
      server_ip = pkt[IPv6].src
      adved_prefix = pkt[ICMPv6NDOptPrefixInfo].prefix
      print '%s RA:  %s(%s)' % (adved_prefix, server_mac, server_ip)

  def run(self):
    sniff(prn=self.handle, filter="icmp6", store=0)

class RASender(object):
  def __init__(self, iface):
    self.srcaddr = get_if_hwaddr(iface)
    conf.iface = iface

  def send(self):
    self.pkt_init()
    sendp(self.msg_disc,verbose=1)

  def pkt_init(self):
    self.msg_disc = (
      Ether(
      src = self.srcaddr, dst="ff:ff:ff:ff:ff:ff")/
      IPv6(dst="ff02::2")/
      ICMPv6ND_RS()
      )

if __name__ == "__main__":
  dh = RAReciver()
  dh.daemon = True
  dh.start()
  d = RASender("eth0")
  d.send()
  time.sleep(1)

