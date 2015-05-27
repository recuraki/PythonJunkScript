#!env python


import json
import sys
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')


url="https://stat.ripe.net/data/bgp-state/data.json?resource="

def parse_resp(dat, addr):
    if "data" in dat:
        if "bgp_state" in dat["data"]:
            parse_resp2(dat["data"]["bgp_state"], addr)

def parse_resp2(dat, addr):
    for d in dat:
        if "path" in d:
            print_path(d["path"], addr)

def print_path(dat, addr):
    print addr + ">" + ",".join(map(lambda x: str(x), dat))

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 2:
        sys.exit(1)
    qurl = url + argv[1]
    fp = urllib2.urlopen(qurl)
    dat = json.loads(fp.read())
    parse_resp(dat, argv[1])

