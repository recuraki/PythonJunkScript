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

# pip install pit
from pit import Pit
# pip instal oauth2
from oauth2 import Client, Token, Consumer
from urllib import urlencode
import os
import sys
import ConfigParser
import json

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
    urlUpdate = "https://api.twitter.com/1.1/statuses/update.json"
    def __init__(self, ckey, csec, ukey, usec):
        self.client = Client(Consumer(ckey, csec),
                             Token(ukey, usec))
    def post(self, content):
        res= self.client.request(self.urlUpdate,
                            'POST',
                            urlencode({"status": content}))
        stRetcode = res[0]['status']
        """
        200 = 成功の場合のみ抜ける
        """
        if stRetcode == "200":
            return(True)
        """
        errorは
        {"errors":[{"code":187,"message":"Status is a duplicate."}]}
        のようにはいる
        """
        liErrors = json.loads(res[1])
        for diError in liErrors.get("errors", []):
            print(diError['message'])




  
if __name__ == "__main__":
    (ckey, csec) = get_Consumersecret()
    tuk = TwitterUserKey()
    (ukey, usec) = tuk.get(ckey, csec)
    twi = Twitter(ckey, csec, ukey, usec)
    print("init end")
    twi.post("hoge2")

