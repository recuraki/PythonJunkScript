#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from scapy.all import *
from time import sleep
import sys
import time
import datetime
import random
import threading

MESSAGE_TYPE_OFFER = 2
MESSAGE_TYPE_REQUEST = 3
MESSAGE_TYPE_ACK = 5
MESSAGE_TYPE_NAK = 6
MESSAGE_TYPE_RELEASE = 7

class DHCPReciver(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self) 

  def handle(handle, pkt):
    if DHCP in pkt:
      mtype = pkt[DHCP].options[0][1]
      your_ipaddr = pkt[BOOTP].yiaddr
      client_mac = pkt.dst
      if mtype == MESSAGE_TYPE_OFFER:
        print '%s DHCP OFFER(transaction:%s): %s for %s from %s' % (num_offers,pkt[BOOTP].xid,your_ipaddr,client_mac,pkt[IP].src)
      elif mtype == MESSAGE_TYPE_ACK:
        pass

      elif mtype == MESSAGE_TYPE_NAK:
        pass

  def run(self):
    sniff(prn=self.handle, filter="udp and (port 68 or port 67)", store=0)
 
class DHCPSender(object):
  def __init__(self, iface):
    self.srcaddr = get_if_hwaddr(iface)
    conf.iface = iface

  def send(self):
    self.pkt_init()
    sendp(self.msg_disc,verbose=0)

  def pkt_init(self):
    xid = random.randint(0, 0xFFFF)
    chaddr = ''.join([chr(int(x,16)) for x in self.srcaddr.split(':')])
    self.msg_disc = (
      Ether(src = chaddr, dst="ff:ff:ff:ff:ff:ff")/
      IP(src="0.0.0.0",dst="255.255.255.255")/
      UDP(sport=68,dport=67)/
      BOOTP(chaddr = chaddr, xid=xid)/
      DHCP(options=[('message-type','discover'),('end')])
      )
"""
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
"""
if __name__ == "__main__":
  dh = DHCPReciver()
  dh.daemon = True
  dh.start()
  time.sleep(0.5)

  d = DHCPSender("eth0")
  d.send()


  time.sleep(1)

