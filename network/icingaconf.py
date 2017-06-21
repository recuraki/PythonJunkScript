#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import optparse
templ="""
define host {{
 use                     generic-host
 host_name               {0}
 alias                   {0}
 address                 {1}
}}
define service {{
 use                     generic-service
 host_name               {0}
 service_description     PING
 check_command           check_ping
}}
"""

def usage():
    print "%s -c <csv_file>" % argv[0]

parser = optparse.OptionParser()
parser.add_option("-c", "--CSVFILE", dest="fn_csv")

(options, args) = parser.parse_args()

fn_csv =  options.fn_csv

if fn_csv == None:
    is_readfromfile = True

fd = open(fn_csv, "r")
dat = fd.read().split("\n")
for l in dat:
    if l == "":
        continue
    c = l.split(",")
    print(templ.format(c[0], c[1]))
