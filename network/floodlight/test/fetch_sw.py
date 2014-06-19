#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

# need: pip install httplib2
import httplib2

debug = 1
def dp(str):
    if debug == 1:
        print(str)

class FloodLightTest(object):
    uri = ""
    def __init__(self, uri):
        self.uri = uri

    def request(self, uri = ""):
        hcQuery = httplib2.Http(".cache")
        response, content = hcQuery.request(uri, "GET")
        self.is_ok(response)
        diContent =  self.deserialize(content)
        dp(diContent)
        
    def deserialize(self, content):
        return json.loads(content)


    def is_ok(self, reResponse, f_exit = True):
        if reResponse.status == 200:
            return True
        if f_exit:
            dp("request failed!")
            sys.exit(1)
        else:
            return false
        

if __name__ == "__main__":
    fl = FloodLightTest("http://test-pin5:8080/")
    fl.request("http://test-pin5:8080/wm/core/controller/switches/json")
        
