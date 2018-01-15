使い方
---
まず、eveにLoginし検査するlabに入っていてください
検査対象になるノードに入っていると、経過が見えます

準備
---
 apt-get install python3-pip python3.5  
 pip3 install PyYAML


FYI: support Japanese on eve-env 
 sudo apt-get install language-pack-ja
 sudo update-locale LANG=ja_JP.UTF-8

使い方
---

python3.5 ./eveGragind.py -e <ipaddr> -f <YAML/dir>
- -e <ipaddr>: 必須
- -f <YAML filename>: 必須 検査対象yamlあるいはディレクトリ

シナリオの記載に関する注意:
---

(などは円マーク\で修飾します。
  しかし、""のなかでは\自信をエスケープする必要があるので、
  \\(などとの表記が必要になります。
例
```
       - "Options: \\(No TOS-capability, DC, Upward\\)"
```

シナリオファイルの書き方
---

あんまり長い結果だと、failします。適当な文字列になるように|incしてください
```
- "hostname": "Router1" #eve上の"nodename"を入れます
  "prompt": "R1" #prompt = hostnameを入れます。expectするのに使われます
  "tests":
   - "name": "addpath enable" #テスト名（結果で表示されます）
     "cmd": "show bgp nei 1.1.1.1" # 実行するコマンド自身です
     "include": # すべて含まれるべき文字列（正規表現）
       - "send capability: received"
       - "Estab"
     "notinclude": # どれかでも含まれてはいけない文字列
       - "receive capability: advertised"
```
