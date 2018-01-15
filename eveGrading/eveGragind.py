#!env python3.5
# -*- coding: utf-8 -*-
from TelnetCheckConfig import TelnetCheckConfig
from Eve import Eve
import yaml
from pprint import pprint
import os
import sys
from optparse import OptionParser


def load_yaml_file(p):
    """
    指定されたファイルを開き、YAMLとして辞書を返す
    :param p: ファイルパス
    :return: 辞書
    """
    with open(p, "r+") as fp:
        r = yaml.load(fp)
        return r
    return None

def complation_ipaddr(d, ipaddr, mappingList):
    """
    構造体dに含まれる"hostname"をkeyとして、
    key:portが格納されたmapping listからport番号を補完する。
    同時に、接続に必要なipaddrの情報も補完する。
    :param d: テスト構造体の辞書
    :param ipaddr: 補完するipaddr
    :param mappingList: {key: port}の辞書
    :return:
    """
    res = []
    for n in d:
        h = n.get("hostname")
        n["port"] = mappingList.get(h)
        n["ipaddr"] = ipaddr
        res.append(n)
    return res

def loadYamlFromDir(p):
    """
    再帰的なYAMLのロード
    ディレクトリの順序関係（おそらくファイル名ソートになるはず)を保持したまま
    ディレクトリの場合は再帰走査する
    ファイルの場合はYAMLとしてロードする
    ファイルからロードされたテストデータはtestsAllに追加される
    :param p:
    :return:
    """
    testsAll = []
    files = os.listdir(p)

    for fn in files:
        fn = os.path.join(p, fn)

        if os.path.isfile(fn): # ファイルの場合の処理
            # .yamlじゃなきゃ、次
            if fn.find(".yaml") < 1:
                continue
            d = load_yaml_file(fn)
            for test in d:
                testsAll.append(test)
            print("  LOAD: {0}".format(fn))
        elif os.path.isdir(fn): # ディレクトリの場合の処理
            print("{0}".format(fn))
            res = loadYamlFromDir(fn)
            for r in res:
                testsAll.append(r)

    return testsAll

def argParser():
    """
    変数をパースし、それらの格納された結果を辞書として返す
    :return:
    """
    arg = {}
    parser = OptionParser()
    parser.add_option("-f", "--file",
                      dest="stFilename", default=None)
    parser.add_option("-e", "--eve",
                      dest="stHost", default=None)
    (options, args) = parser.parse_args()
    arg["stFilename"] = options.stFilename
    arg["stHost"] = options.stHost
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
        evehost = args["stHost"]
    if evehost is None:
        pprint("NEED: -e <evehost>")
        sys.exit(-1)
    pprint("EVE HOSTADDR = " + evehost)


    # 条件: fileがdirが指定されていること
    if args["stFilename"] is None:
        pprint("NEED: -f <yaml>")
        #sys.exit(-1)
    stFilename = args["stFilename"]

    # eveホストに接続し、mappingリスト及び、開くべきlab nameを取得する
    e = Eve(evehost)
    conRes = e.connect()
    d= e.get_nodelist()
    mappingList = e.parse_nodelist2port(d)

    # 指定されたファイル・ディレクトリを読み込む
    if os.path.isfile(stFilename):
        print("LOAD: {0}".format(stFilename))
        testsAll = load_yaml_file(stFilename)
    elif os.path.isdir(stFilename):
        print("{0}".format(stFilename))
        testsAll = loadYamlFromDir(stFilename)

    # 読み込んだテスト情報に対してホスト名とポート番号を補完する
    testsAll = complation_ipaddr(testsAll, evehost, mappingList)

    # すべてのテストケースに対してテストを実施
    for t in testsAll:
        tcc = TelnetCheckConfig(debug=False)
        (node, is_pass, res) = tcc.test(t)
        tcc.writeResult(res)
        tcc.writeResult2stdout(res)
        tcc.disconnect()
        tcc = None