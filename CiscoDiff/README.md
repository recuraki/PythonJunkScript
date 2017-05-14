Cisco Diff
-----------

- 概要

Cisco 無印/XE系のOSのshow runなどは、階層構造を持っている。
ただし、それらはスペースで階層化されたテキスト構造であり、
視覚的に理解はしやすいものの、ソフトウェアで扱うには階層的な読み込みを行う必要がある。

このプロジェクトでは、読み込むためのライブラリに加えて、
CiscoのConfigを扱うのによく用いられるいくつかのアプリケーションを提供する。

1. Cisco形式のファイルを読み込むライブラリ
1. beforeとafterのファイルを比較し、afterにするために必要なコマンドセットを生成
1. beforeとafterのファイルを比較し、それがあらかじめ定義した差分であるtest通りの変更であるかを比較


 - testファイルの書き方(YAML)

テストファイルはYAML形式にて、それぞれaddとdelという辞書に
予期するConfigの辞書を記載する。
それぞれ階層的な辞書で記載する。
「終わり」の階層においても空の辞書として定義する。

 ```
 add:
   "interface Loopback0":
     "desctiption loopback":
   "ip nat translation timeout 600":
＃del/addがない場合は空の辞書とすればよい
 del:
 ```
