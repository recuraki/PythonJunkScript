#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

# need: pip install httplib2
import httplib2

# デバッグコード
debug = 1

def dp(str):
    if debug == 1:
        print(str)

class FloodLightTest(object):
    """
    テスト用のReST APIライブラリ
    """
    
    uri = ""
    
    def __init__(self, uri):
        """
        Objectは生成時にuriを求める
        """
        self.uri = uri

    def request(self, uri = ""):
        hcQuery = httplib2.Http(".cache")
        # レスポンスコードとコンテンツの取得
        response, content = hcQuery.request(uri, "GET")
        # レスポンスコードの確認
        self.is_ok(response)
        # json -> python辞書
        diContent =  self.deserialize(content)
        dp(diContent)
        
    def deserialize(self, content):
        """
        json -> python辞書
        """
        return json.loads(content)

    def is_ok(self, reResponse, f_exit = True):
        """
        HTTP return codeの確認 200以外はfailと見なす
        """
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
    
