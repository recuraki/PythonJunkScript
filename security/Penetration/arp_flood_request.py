#!/usr/local/bin/python


from scapy.all import *
import ipaddress


targetnet = u"172.16.1.0/25"

liHosts = list(ipaddress.ip_network(targetnet).hosts())

print liHosts

for pdsthost in liHosts:
    pdsthost = str(pdsthost)

    #srcmac = RandMAC()
    dstmac = "ff:ff:ff:ff:ff:ff"
    
    sendp(Ether(dst=dstmac)/ARP(op=1, pdst=pdsthost, hwdst=dstmac)/Padding(load="X"*18))
