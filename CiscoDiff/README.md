Cisco Diff
-----------

- 概要

Cisco IOS/XE系のOSのshow runなどは、階層構造を持っている。

それらはスペースで階層化されたテキスト構造であり、
視覚的に理解はしやすいものの、ソフトウェアで扱うには階層的な読み込みを行う必要がある。

このプロジェクトでは、読み込むためのライブラリに加えて、
CiscoのConfigを扱うのによく用いられるいくつかのアプリケーションを提供する。

1. Cisco形式のファイルを読み込むライブラリ
1. beforeとafterのファイルを比較し、afterにするために必要なコマンドセットを生成
1. beforeとafterのファイルを比較し、それがあらかじめ定義した差分であるtest通りの変更であるかを比較


- つかいかた

CiscoContextualDiff.pyはコマンドラインのツールを提供する。

```
./CiscoContextualDiff.py -b <beforeconfig> -a <afterconfig> [-v <verify file>] [-g] [-o <outfile>] [-d]
```

|結果|意味|
|--|--|
|EXTRA-ADD|本来追加されるはずではないのに追加された|
|EXTRA-DELETE|本来削除されないはずなのに削除された|
|EXPECT ADD BUT NOT ADD|追加されるはずなのに追加されていない|
|EXPECT DELETE BUT NOT DELETE|削除されるはずなのに削除されていない|


- 単なる比較
```
./CiscoContextualDiff.py -b sample_before2 -a sample_after2
EXTRA-ADD
{('interface Loopback0', 'ip ospf cost 1'),
 ('interface Loopback4',),
 ('interface Loopback4', 'shutdown')}
EXTRA-DELETE
{('interface Loopback0', 'ip ospf cost 10'),
 ('interface Loopback2',),
 ('interface Loopback2', 'shutdown'),
 ('interface Loopback3', 'shutdown')}
!!!!!!!!! NG !!!!!!!!!
```

- テストファイルを用いた比較

まず、テストファイルを以下のように準備する。
```
./CiscoContextualDiff.py -b sample_before2 -a sample_after2 -g -o v
[add]
interface Loopback0 | ip ospf cost 1
interface Loopback4
interface Loopback4 | shutdown
[delete]
interface Loopback0 | ip ospf cost 10
interface Loopback2
interface Loopback2 | shutdown
interface Loopback3 | shutdown
```
このコマンドにより、先述のような差分を意味するテストファイルが生成される。
この際、各階層構造は" | "で分割される。

-gのみを指定すると、プログラムはテストファイル形式での差分を標準出力のみに出力する。

-gと-oを同時に指定した場合は、さらに-oの引数にその結果を出力する。

テストファイルは
```
[addかdelete]
階層1 | 階層2 | ... | 階層n
階層1 | 階層2 | ... | 階層n
```
のように書かれるべきである。このファイルを使って検証を行う。

```
[kanai@www:25747]./CiscoContextualDiff.py -b sample_before2 -a sample_after2 -v v
OK: SAME CONFIG
```

つぎに、上記のファイルからLoopback4とinterface Loopback0 | ip ospf cost 10の行を恣意的に消して、
Loopback8を削除、Loopback9を追加すべきだというように書き換える。

```
[kanai@www:25756]cat v
[add]
interface Loopback0 | ip ospf cost 1
interface Loopback9
[delete]
interface Loopback2
interface Loopback2 | shutdown
interface Loopback3 | shutdown
interface Loopback8
[kanai@www:25757]./CiscoContextualDiff.py -b sample_before2 -a sample_after2 -v v
EXTRA-ADD
{('interface Loopback4',), ('interface Loopback4', 'shutdown')}
EXPECT ADD BUT NOT ADD
{('interface Loopback9',)}
EXTRA-DELETE
{('interface Loopback0', 'ip ospf cost 10')}
EXPECT DELETE BUT NOT DELETE
{('interface Loopback8',)}
!!!!!!!!! NG !!!!!!!!!
```

