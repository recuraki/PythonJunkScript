#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
使い方:
TwitterでApplicationを登録して、Consumer KeyとSecretを得ます。
プログラムを実行すると、これらを入力するeditorが(pitによって)起動されるので、
これらを書き込みます(ちなみに""は不要です)
もし、編集に失敗した場合、
~/.put/defautなどを消してください

次に、URLが表示されて
PIN:
と言われます。これはUserごとのTokenを得るためです。

ブラウザでPINを得たら、入力します。
"""


# 以下を参考にしました。
# http://d.hatena.ne.jp/reppets/20100522/1274553529

# oauth2のライブラリの編集をする
# http://blog.livedoor.jp/iakyi/archives/4111571.html
#
# /Library/Python/2.7/site-packages/oauth2/__init__.py
#

from __future__ import unicode_literals

# pip install pit
from pit import Pit
# pip instal oauth2
from oauth2 import Client, Token, Consumer
from urllib import urlencode
import os
import sys
import ConfigParser
import json
import pickle
import datetime
import types


import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

"""
pitを使うのでEDITORを必須にする
"""
if not "EDITOR" in os.environ:
  print("OS-EDITOR = NONE")
  #sys.exit(1)

def get_Consumersecret():
    """
    pitからcustomer keyを呼ぶ
      """
    piConf = Pit.get("twitter-consumer", {'require':
                                 {'ckey': 'ConsumerKey',
                                  'csecret': 'ConsumerSecret'
                                  }})
    return(piConf['ckey'], piConf['csecret'])


class TwitterUserKey():
  """
  oauth用のクラス。
  """
  ukey = ""
  usecret = ""
  urlReqToken = "https://api.twitter.com/oauth/request_token"
  urlReqPin = "https://api.twitter.com/oauth/authorize?oauth_token="
  urlReqKey = "https://api.twitter.com/oauth/access_token"
  configname = "./.cache.basic"

  def __init__(self):
    pass

  def getfromcfg(self):
      """
      既存の設定ファイルにuser key情報が含まれていたらそちらから取得する
      """
      cfg = ConfigParser.SafeConfigParser()
      res = cfg.read(self.configname)
      # Twitter sectionがない＝ファイルが生成されていないと判断する
      if not cfg.has_section("twitter"):
          return("", "")
      ukey = cfg.get("twitter", "ukey", "")
      usec = cfg.get("twitter", "usec", "")
      return(ukey, usec)

  def setcfg(self, ukey, usec):
      """
      設定ファイルにuserのtoken情報を書き込む
      """
      cfg = ConfigParser.SafeConfigParser()
      cfg.add_section("twitter")
      cfg.set("twitter", "ukey", ukey)
      cfg.set("twitter", "usec", usec)
      cfg.write(open(self.configname, "w"))

  def get(self, ckey, csec):
    """
    oauthを行う。
    tokenを要求した後、PINの入力を受付け、
    その結果、token情報を返す
    """

    """
    リプライをパースするλ式
    oauth_token=IE&oauth_token_secret=0x&oauth_callback_confirmed=true'
    を
    {'oauth_token_secret': '0x', 'oauth_token': 'IEb', 'oauth_callback_confirmed': 'true'}
    のようにする
    """
    parseparam = lambda x: dict(map(lambda y: y.split('='), x.split("&")))

    # 設定ファイルに情報があるならそこからもらい返す
    ukey, usec = self.getfromcfg()
    if ukey != "" and usec != "":
      return( (ukey, usec) )

    # oauth用のクラス定義
    client = Client(Consumer(ckey, csec), None)

    # トークンの要求
    liRes = client.request(self.urlReqToken,
                        'GET')
    diRes = parseparam(liRes[1])

    # 得たトークンを基にPINの要求を行う
    request_token = Token(diRes["oauth_token"], diRes["oauth_token_secret"])
    print("plz access: " + self.urlReqPin + request_token.key)
    stPin = raw_input('PIN:')
    request_token.set_verifier(stPin)

    # 実際のキーをもらう
    client.token = request_token
    liRes = client.request(self.urlReqKey,
                        'POST')
    # 情報をパースする
    diRes = parseparam(liRes[1])
    ukey = diRes["oauth_token"]
    usec = diRes["oauth_token_secret"]

    # 設定ファイルに書き込む
    self.setcfg(ukey, usec)

    return(
        (ukey,
        usec,
        diRes["user_id"],
        diRes["screen_name"])
    )

class Twitter(object):

    fnCache = "./.cache.twitter"
    objCache = {}
    urlUpdate = "https://api.twitter.com/1.1/statuses/update.json"
    urlFriendIds = "https://api.twitter.com/1.1/friends/ids.json"
    urlSearchTweet = "https://api.twitter.com/1.1/search/tweets.json"

    def _override_tourl(self):
        """Serialize as a URL for a GET request."""
        base_url = urlparse.urlparse(self.url)
        try:
            query = base_url.query
        except AttributeError:
            # must be python <2.5
            query = base_url[4]
        query = parse_qs(query)
        for k, v in self.items():
            query.setdefault(k, []).append(v)

        try:
            scheme = base_url.scheme
            netloc = base_url.netloc
            path = base_url.path
            params = base_url.params
            fragment = base_url.fragment
        except AttributeError:
            # must be python <2.5
            scheme = base_url[0]
            netloc = base_url[1]
            path = base_url[2]
            params = base_url[3]
            fragment = base_url[5]

        url = (scheme, netloc, path, params,
               urllib.urlencode(query, True), fragment)
        return urlparse.urlunparse(url)

    def __init__(self, ckey, csec, ukey, usec, use_cache = True):
        self.client = Client(Consumer(ckey, csec),
                             Token(ukey, usec))

        self.client.to_url = self._override_tourl

        try:
            f = open(self.fnCache, 'rb')
        except IOError:
            print("no cache file")
            self._write_Cache()
        else:
            self.objCache = pickle.load(f)

    def _write_Cache(self):
        with open(self.fnCache, 'wb') as f:
            pickle.dump(self.objCache, f)

    def _set_Cache(self, name, val):
        print("setCache:" + name + "-" + val)
        curDate = datetime.datetime.now()
        self.objCache[name] = (curDate, val)

    def _get_Cache(self, name, timeout = 0):
        print("getCache:" + name )

        # キャッシュがそもそも存在しなければNoneを返す
        if not name in self.objCache:
            return None

        # 現在の時刻とキャッシュの時刻を比較する
        curDate = datetime.datetime.now()
        (cacheDate, val ) = self.objCache[name]
        deltaDate = curDate - cacheDate

        # 指定されたキャッシュ期限をすぎていた場合、なにも返さない
        if deltaDate.seconds > timeout:
            return None

        # キャッシュ期間内であればキャッシュの値を返す
        return val

    def _handle_error(self, stErrors):
        """
        errorは
        {"errors":[{"code":187,"message":"Status is a duplicate."}]}
        のようにはいる
        """
        liErrors = json.loads(stErrors)
        for diError in liErrors.get("errors", []):
            print(diError['message'])

    def post(self, content):
        res = self.client.request(self.urlUpdate,
                            'POST',
                            urlencode({"status": content}))
        stRetcode = res[0]['status']
        # 200のときのみ抜ける
        if stRetcode == "200":
            return(True)
        self._handle_error(res[1])

    def get_friend_ids(self):
        friend_ids = self._get_Cache("friend_ids", timeout=1800)
        if friend_ids:
            return friend_ids

        res = self.client.request(self.urlFriendIds,
                        'GET')
        stRetcode = res[0]['status']
        # 200のときのみ抜ける
        if stRetcode == "200":
            friend_ids = res[1]

        self._set_Cache("friend_ids", friend_ids)
        self._write_Cache()
        return friend_ids

        # print json.dumps(res, indent=4)

    def search_tweets(self, keyword):
        args = dict()
        args["q"] = "ほげ"
        #args["result_type"] = "recent"
        #args["count"] = "10"
        #args["include_entities"] = "True"

        params = urlencode(dict([k, v.encode('utf-8') if isinstance(v, unicode) else v] for k, v in args.items()))

        """
        params={}
        print args
        for k, v in args.iteritems():
            if isinstance(v, unicode):
                params[k] = unicode(v).encode('utf-8')
            else:
                params[k] = v
        params = urlencode(params)
        """

        print params


        url = self.urlSearchTweet + "?" + params
        url = "https://api.twitter.com/1.1/search/tweets.json?q=%e3%82%82%e3%81%92"
        print url

        res = self.client.request(url)
        print json.dumps(res, indent=4)


if __name__ == "__main__":
    # Twitterオブジェクトに渡すキーの初期化
    (ckey, csec) = get_Consumersecret()
    tuk = TwitterUserKey()
    (ukey, usec) = tuk.get(ckey, csec)

    # Twitterクライアントオブジェクトの生成
    twi = Twitter(ckey, csec, ukey, usec)

    print("init end")

    #twi.post("hoge")
    #twi.search_tweets("#test")
    #print twi.get_friend_ids()


