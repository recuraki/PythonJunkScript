#!/usr/bin/python
# -*- coding: utf-8 -*-

from scapy.all import *
from time import sleep

p = (Ether(src="00:0c:29:00:00:00",dst="00:00:5e:00:00:00")/IP(src="10.0.0.20",dst="172.16.0.20")/ICMP(type = 8, seq=1))
sendp(p, verbose=1, iface="eth1")
print(p.show())

