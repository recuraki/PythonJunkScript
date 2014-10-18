#!/usr/local/bin/python
# -*- coding: utf-8 -*-

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

if not "EDITOR" in os.environ:
  print("OS-EDITOR = NONE")
  #sys.exit(1)

def get_Consumersecret():
  piConf = Pit.get("twitter-consumer", {'require':
                                 {'ckey': 'ConsumerKey',
                                  'csecret': 'ConsumerSecret'
                                  }})
  return(piConf['ckey'], piConf['csecret'])


class TwitterUserKey():
  ukey = ""
  usecret = ""
  urlReqToken = "https://api.twitter.com/oauth/request_token"
  urlReqPin = "https://api.twitter.com/oauth/authorize?oauth_token="
  urlReqKey = "https://api.twitter.com/oauth/access_token"
  configname = "./.cache.basic"

  def __init__(self):
    pass

  def getfromcfg(self):
      cfg = ConfigParser.SafeConfigParser()
      res = cfg.read(self.configname)
      if not cfg.has_section("twitter"):
          return("", "")
      ukey = cfg.get("twitter", "ukey", "")
      usec = cfg.get("twitter", "usec", "")
      return(ukey, usec)


  def setcfg(self, ukey, usec):
      cfg = ConfigParser.SafeConfigParser()
      cfg.add_section("twitter")
      cfg.set("twitter", "ukey", ukey)
      cfg.set("twitter", "usec", usec)
      cfg.write(open(self.configname, "w"))

  def get(self, ckey, csec):
    """
    リプライをパースするλ式
    oauth_token=IE&oauth_token_secret=0x&oauth_callback_confirmed=true'
    を
    {'oauth_token_secret': '0x', 'oauth_token': 'IEb', 'oauth_callback_confirmed': 'true'}
    のようにする
    """
    parseparam = lambda x: dict(map(lambda y: y.split('='), x.split("&")))

    ukey, usec = self.getfromcfg()

    if ukey != "" and usec != "":
      return( (ukey, usec) )

    consumer = Consumer(ckey, csec)
    client = Client(consumer, None)

    liRes = client.request(self.urlReqToken,
                        'GET')
    diRes = parseparam(liRes[1])

    request_token = Token(diRes["oauth_token"], diRes["oauth_token_secret"])
    print("plz access: " + self.urlReqPin + request_token.key)
    stPin = raw_input('PIN:')
    request_token.set_verifier(stPin)

    client.token = request_token

    liRes = client.request(self.urlReqKey,
                        'POST')
    diRes = parseparam(liRes[1])
    print diRes

    ukey = diRes["oauth_token"]
    usec = diRes["oauth_token_secret"]

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
        print res

  
if __name__ == "__main__":
    (ckey, csec) = get_Consumersecret()
    tuk = TwitterUserKey()
    (ukey, usec) = tuk.get(ckey, csec)
    twi = Twitter(ckey, csec, ukey, usec)
    print("init end")
    twi.post("hoge")

