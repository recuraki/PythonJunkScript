はじめに
===========
ペネトレーションテストのためです。

SubspeciesPassword.py
=========================

パスワードのペネトレーションテストのために、
与えられた文字列から推測される文字列を生成します。

```text
./SubspeciesPassword.py hoe
hoe
hoE
ho3
hOe
hOE
(cont..)
```

sample{SSH,Telnet}.py
================================

telnet/SSHのペネトレーションテストのために、
引数に与えられたcsvファイルのusername,passwordの対を元に、
ホストに対してアクセスを試みます。
[OK]は成功したパスワードを表示します。

```text
./sampleTelnet.py resourcePassword.csv
./sampleSSH.py resourcePassword.csv
Try]: user
Try]: user2
Try]: user999
OK]: user999
Try]: user1000
```
