#!env python3.5
# -*- coding: utf-8 -*-
from TelnetCheckConfig import TelnetCheckConfig
from Eve import Eve
import yaml
from pprint import pprint
import os
import sys
from optparse import OptionParser
from pathlib import Path

def argParser():
    """
    変数をパースし、それらの格納された結果を辞書として返す
    :return:
    """
    arg = {}
    parser = OptionParser()
    parser.add_option("-d", "--dir",
                      dest="stFilename", default=None)
    parser.add_option("-e", "--eve",
                      dest="stHost", default=None)
    parser.add_option("-m", "--mapping",
                      dest="stMapping", default=None)
    (options, args) = parser.parse_args()
    arg["stFilename"] = options.stFilename
    arg["stHost"] = options.stHost
    arg["stMapping"] = options.stMapping
    return arg

if __name__ == "__main__":
    # 引数の処理
    args = argParser()

    # 設定ファイルを読み込む
    try:
        with open("eveDefault.yaml", "r+") as fp:
            defaultValue = yaml.load(fp)
            fp.close()
    except FileNotFoundError:
        print("eveDefault.yaml is not found")
        defaultValue = {}

    # evehostの読み込み(defaultに設定があるならそこから読み込む
    evehost = defaultValue.get("evehost", None)
    if args["stHost"] is not None:
        evehost == args["stHost"]
    if evehost is None:
        pprint("NEED: -e <evehost>")
        sys.exit(-1)

    basepath = defaultValue.get("dirDumpTo", "./")
    subdir = "" if args["stFilename"] is None else args["stFilename"]
    savepath = Path(basepath) / Path(subdir)
    if savepath.exists() == False:
        pprint("Create: " + str(savepath))
        savepath.mkdir()

    mappingFile = defaultValue.get("mappingFile", "host-prompt.yaml")
    if args["stMapping"] is not None:
        mappingFile = args["stMapping"]
    try:
        with open(mappingFile, "r+") as fp:
            promptMapping = yaml.load(fp)
    except FileNotFoundError:
        promptMapping = {}
        print ("{0} is not found: NOMAPPING".format(mappingFile))

    # eveホストに接続し、mappingリスト及び、開くべきlab nameを取得する
    e = Eve(evehost)
    conRes = e.connect()
    d= e.get_nodelist()

    mappingList = e.parse_nodelist2port(d, statusFilter=2)

    for hostname in mappingList:
        prompt = promptMapping.get(hostname, hostname)
        if prompt == None:
            print("SKIP: " + hostname)
            continue
        print("Try: " + hostname + " (Prompt:{0})".format(prompt))
        port = mappingList[hostname]
        tcc = TelnetCheckConfig(debug=False)
        index, pat, res = tcc.showRun(evehost, port, prompt, timeout=3)
        if pat != None:
            fn = savepath / Path(hostname)
            print(" PASS: save to " + str(fn))
            with fn.open(mode = "w", encoding = "utf-8") as fw:
                # first 2 lines and last 2 lines will be snip :p
                contents = res.split("\n")
                contents = "\n".join(contents[2:-2])
                fw.write(contents)
                fw.close()
        else:
            print ("FAIL: PROMPT LOST")
