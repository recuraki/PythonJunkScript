#!/usr/local/bin/python


from scapy.all import *
import ipaddress


targetnet = u"192.168.1.0/24"

liHosts = list(ipaddress.ip_network(targetnet).hosts())

print liHosts

for pdsthost in liHosts:
    pdsthost = str(pdsthost)

    #srcmac = RandMAC()
    dstmac = "ff:ff:ff:ff:ff:ff"
    
    sendp(Ether(dst=dstmac)/ARP(op=1, pdst=pdsthost, hwdst=dstmac)/Padding(load="X"*18))
