#! env python3

import uuid
import urllib.parse
import requests
import platform
import sys

from secret import csec, ckey
print(csec)

def authorize(client_id, client_secret):
    """
    see:
    http://qiita.com/icoxfog417/items/1f5d7d4e5758deca349b
    """
    url = "https://oxford-speech.cloudapp.net//token/issueToken"
    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }

    params = urllib.parse.urlencode(
        {"grant_type": "client_credentials",
         "client_id": ckey,
         "client_secret": csec,
         "scope": "https://speech.platform.bing.com"}
    )

    response = requests.post(url, data=params, headers=headers)
    if response.ok:
        _body = response.json()
        return _body["access_token"]
    else:
        response.raise_for_status()
        
def speech_to_text( binary, token, lang="en-US", samplerate=8000, scenarios="ulm"):
    data = binary
    params = {
        "version": "3.0",
        "appID": "D4D52672-91D7-4C74-8AD8-42B1D98141A5",
        "instanceid": "1ECFAE91408841A480F00935DC390960",
        "requestid": "b2c95ede-97eb-4c88-81e4-80f32d6aee54",
        "format": "json",
        "locale": lang,
        "device.os": "Windows7",
        "scenarios": scenarios,
    }

    url = "https://speech.platform.bing.com/recognize/query?" + urllib.parse.urlencode(params)
    headers = {"Content-type": "audio/wav; samplerate={0}".format(samplerate),
               "Authorization": "Bearer " + token,
               "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
               "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
               "User-Agent": "OXFORD_TEST"}

    response = requests.post(url, data=data, headers=headers)

    if response.ok:
        print(response.json())
        result = response.json()["results"][0]
        return result["lexical"]
    else:
        raise response.raise_for_status()

fdr = open("jp.wav", "rb")
data = fdr.read()

token = authorize(ckey, csec)

res = speech_to_text(data, token, lang="ja-JP")
print(res)
