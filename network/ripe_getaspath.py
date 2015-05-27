#!env python
# -*- coding: utf-8 -*-

import json
import sys
import urllib2
import optparse

reload(sys)
sys.setdefaultencoding('utf-8')

# デフォルトのapi-URL
url="https://stat.ripe.net/data/bgp-state/data.json?resource="

def parse_resp(dat, addr, opts):
    """
    入力を受けて、as_pathがあるか確認
    """
    if "data" in dat:
        if "bgp_state" in dat["data"]:
            parse_resp2(dat["data"]["bgp_state"], addr, opts)

def parse_resp2(dat, addr, opts):
    """
    2段目
    """
    l = []
    graph_con = []
    # bgp_stateのそれぞれのas_pathを文字列で得る
    # 結果はlにリストで入る
    for d in dat:
        if "path" in d:
            r = get_path(d["path"], addr, opts)
            s = ">".join(map(lambda x: str(x), r))
            l.append(s)
            p = ""
            for d in r:
                if p != "":
                    graph_con.append((str(p), str(d)))
                p = d

    # lから重複を削除する
    l = list(set(l))
    graph_con = list(set(graph_con))

    if opts.f_graph:
        o = []
        for d in graph_con:
            o.append("->".join(list(d)))
        print(",".join(o))
        return()

    # 表示する
    for d in l:
      print addr + ":" + d

def get_path(dat, addr, opts):
    # as_pathはoriginが最後なので、逆にする
    dat.reverse()
    # prependを排除
    if opts.f_uniq:
        dat = del_uniq(dat)
    # limit個までしか表示しない
    dat = dat[:int(opts.o_length)]
    # ">"でAS_PATHを結合する
    return(dat)

def del_uniq(dat):
    """
    重複を排除する。
    2500,2500,2500 -> 2500
    """
    p = ""
    l = []
    for d in dat:
        if p != d:
            l.append(d)
            p = d
    return(l)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-l", "--length", dest="o_length", action="store", default="250")
    parser.add_option("-u", "--unique", dest="f_uniq", action="store_true", default=False)
    parser.add_option("-g", "--graph", dest="f_graph", action="store_true", default=False)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        sys.exit(1)
    qurl = url + args[0]
    fp = urllib2.urlopen(qurl)
    dat = json.loads(fp.read())
    parse_resp(dat, args[0], options)

