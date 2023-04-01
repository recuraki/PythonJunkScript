import webvtt
import requests

API_KEY = 'xxxxxx' # 自身の API キーを指定

text = "Riemann Zeta function is a very important function in number theory."
source_lang = 'EN'
target_lang = 'JA'

# パラメータの指定
params = {
            'auth_key' : API_KEY,
            'text' : text,
            'source_lang' : source_lang, # 翻訳対象の言語
            "target_lang": target_lang  # 翻訳後の言語
        }




vtt = webvtt.read('test.vtt')
print("Read {} sentenses".format(len(vtt)))
memory = []
cur = []
for i in range(len(vtt)):
    x = vtt[i]
    text = x.text
    params["text"] = text
    request = requests.post("https://api-free.deepl.com/v2/translate", data=params)  # URIは有償版, 無償版で異なるため要注意
    result = request.json()
    print(result)
    texts = result["translations"]
    jpstr = ""
    for x in texts:
        jpstr += x["text"]
    print("{} / {}".format(i, len(vtt)))
    print("<- {}".format("You are a helpful assistant that translates English to Japanese. - " + text))
    print("-> {}".format(jpstr))
    vtt[i].text = jpstr

with open('my_captions.vtt', 'w') as fd:
    vtt.write(fd, format="vtt")