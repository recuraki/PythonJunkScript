#! env python3

import uuid
import urllib.parse
import requests
import platform

from secret import csec, ckey
print(csec)
if not "EDITOR" in os.environ:
  print("OS-EDITOR = NONE")
  #sys.exit(1)

def get_Consumersecret():
    piConf = Pit.get("azure-speech", {'require':
                                 {'ckey': 'ConsumerKey',
                                  'csecret': 'ConsumerSecret'
                                  }})
    return(piConf['ckey'], piConf['csecret'])


if True:
    (ckey, csec) = get_Consumersecret()
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
        

    print(authorize(ckey, csec))
