#!/usr/bin/python
# coding: utf-8

import dpkt
import sys
import dpkt
import socket, random
import binascii
import struct

def sum_hex(stHex):
    """
    'abcd1234'という可変文字列を
    0xabcd + 0x1234してretする
    """
    c = 0
    sum = 0
    for i in range(0, len(stHex), 4):
        """
        'abcd1234'という文字列を
        0xab * 256 + 0xcd = 0xabcdとする
        """
        c = 256 * int(stHex[i:i + 2], 16)
        c = c +  int(stHex[i + 2: i + 4], 16)
        #print("%04x" % c)
        # で、全部足す
        sum = sum + c
    return(sum)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need pcapfile")
        sys.exit(0)

    fd = open(sys.argv[1])
    pcap = dpkt.pcap.Reader(fd)

    inCount = 0
    
    for ftTime, buf in pcap:
        inCount += 1
        print("Packet[{0}]".format(inCount))
        eth = dpkt.ethernet.Ethernet(buf)
        if type(eth.data) == dpkt.ip6.IP6:
            ipv6 = eth.data
            cksum = 0
            cksum += sum_hex(binascii.hexlify(str(ipv6.src)))
            cksum += sum_hex(binascii.hexlify(str(ipv6.dst)))
            cksum += 58
            ipv6_src = socket.inet_ntop(socket.AF_INET6, ipv6.src)
            ipv6_dst = socket.inet_ntop(socket.AF_INET6, ipv6.dst)
            print("[Host] {0}->{1}".format(ipv6_src, ipv6_dst))
            if type(ipv6.data) == dpkt.icmp6.ICMP6:
                icmp6 = ipv6.data
                print("Type:{0}, Code:{1}, CurrentChecksum:{2}".format(icmp6.type, icmp6.code,
                                                                       "%04x" % icmp6.sum))
                stHex = binascii.hexlify(str(icmp6.data))
                cksum += icmp6.type * 256 + icmp6.code
                cksum += len(icmp6)
                cksum += sum_hex(stHex)
            #print("%04x - %04x + %04x" % (int("ffff",16) , (cksum >> 16),  (cksum & int("ffff", 16))))
            cksum =  int("ffff",16) - ( (cksum >> 16)  + ((cksum & int("ffff", 16))))
            print("CALCed Checksum: %04x" % cksum)
            print("--------------")
