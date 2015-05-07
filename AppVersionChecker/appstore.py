#!env python
# -*- coding: utf-8 -*-

# 文字コード対策
import sys
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')

class appstore(object):
    urlBase = "https://itunes.apple.com/search?term={0}&entity=software"

    def __init__(self):
        pass

    def fetch(self, hint):
        fp = urllib2.urlopen(self.urlBase.format(hint))
        dat = fp.read()
        print dat

if __name__ == "__main__":
    c = appstore()
    c.fetch("")
