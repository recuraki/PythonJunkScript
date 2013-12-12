#!/usr/bin/python
# coding: utf-8

import dpkt
import sys
import dpkt
import socket, random
import binascii
import struct

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need pcapfile")
        sys.exit(0)

    fd = open(sys.argv[1])
    pcap = dpkt.pcap.Reader(fd)

    for ftTime, buf in pcap:
        print ftTime, len(buf)
        eth = dpkt.ethernet.Ethernet(buf)
        if type(eth.data) == dpkt.ip6.IP6:
            print "IPv6"
            ipv6 = eth.data
            ipv6_src = socket.inet_ntop(socket.AF_INET6, ipv6.src)
            ipv6_dst = socket.inet_ntop(socket.AF_INET6, ipv6.dst)
            print(ipv6_src + "->" + ipv6_dst)
            print(type(ipv6.data))
            if type(ipv6.data) == dpkt.icmp6.ICMP6:
                pass
            
        sys.exit(1)
