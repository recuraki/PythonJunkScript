#!/usr/bin/python
# -*- coding: utf-8 -*-

host = "192.168.48.135"

import os
import sys
import re
import json
from urllib.request import build_opener, HTTPCookieProcessor
from urllib.parse import urlencode
from http.cookiejar import CookieJar
import pprint
from pprint import pprint

class Eve():
    """
    eveのAPIクラス
    """
    host = None
    eve_user = "admin"
    eve_pass = "eve"
    opener = None
    lab = None
    lab = ""
    isDebug = False

    def __init__(self, host, isDebug = False):
        """
        :param host: ホスト名
        """
        self.host = host
        self.isDebug = isDebug

    def connect(self):
        """
        authを行う
        :return:
        """

        # cookie付きのオープンハンドラ
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()))
        o = {}
        o["username"] = self.eve_user
        o["password"] = self.eve_pass
        o["html5"] = "-1"
        stJson = json.dumps(o).encode("utf-8")
        headers = {}
        headers["Content-Type"] = "application/json"

        #　ログインの試行
        u = "http://{0}/api/auth/login".format((self.host))
        res = self.opener.open(u, stJson)
        self.dprint(res.getheaders())

        # 現在開いているlabの取得
        u = "http://{0}/api/auth".format((self.host))
        res = self.opener.open(u)
        self.dprint(res.getheaders())
        response_body = res.read().decode("utf-8")
        self.dprint(response_body)
        d = json.loads(response_body)
        data = d.get("data", {})
        self.lab = data.get("lab", "")


    def get_nodelist(self):
        # [GET] ノード情報の取得
        u = "http://{0}/api/labs/{1}/nodes".format(self.host, self.lab)
        self.dprint(">> [{0}]".format(u))

        res = self.opener.open(u, timeout=3)

        self.dprint(res.getheaders())
        response_body = res.read().decode("utf-8")
        self.dprint(response_body)
        d = json.loads(response_body)
        if d["code"] != 200:
            sys.exit(1)
        return(d)

    def disconnect(self):
        pass

    def set_lab(self, lab):
        self.lab = lab

    def parse_nodelist2port(self, data, statusFilter = None):
        # 取得したノード一覧をnodename : portに変換する補助関数
        allnodes = data["data"]
        nodes = {}
        for id in allnodes:
            node = allnodes[id]

            # statusFilterが指定されている場合、そのstatusだけを処理する
            if statusFilter is not None:
                if node.get("status", None) != statusFilter:
                    continue
            hostname = node["name"]
            port = node.get("url", "").split(":")[2]
            nodes[hostname] = port
        return nodes

    def dprint(self, str):
        if self.isDebug:
            pprint(str)

if __name__ == "__main__":
    e = eve(host)
    e.connect()
    d= e.get_nodelist()
    dat = e.parse_nodelist2port(d)
    for h in dat:
        print("{0}-{1}".format(str(h), dat[h]))
