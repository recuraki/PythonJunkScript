#!/usr/local/bin/python

from scapy.all import *
# [get_if_hwaddr(i) for i in get_if_list()]

for if_name in get_if_list():
  print if_name + ": " + get_if_hwaddr(if_name)
