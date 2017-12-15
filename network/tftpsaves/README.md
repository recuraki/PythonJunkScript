
tftpsave
==

何十台かのルータなどのcopy tftp...を実施します。


セールスポイント
--

- 非同期で情報を取ってきます。
- pexpectのasyncはあんまり例がないです。

使い方
--

./main.py [-c] [-p] [-s]

- -c(--CONFIG): 設定ファイルのパスです
- -p(--PREFIX): ファイル名につける前文字列を指定します
- -s(--SUFFIX): ファイル名につける後文字列を指定します

設定ファイル
--
```
global:
 # tftpするサーバのアドレス
 tftpserver: "192.168.196.99"
 # Slack通知のメッセージ作成(不要なら指定不要)
 # slackmode = all だったら実施のたびにログを出す
 # slackmode = error の時はエラーだけしか返さない
 slackmode: "error"
 # webhookのURL
 slackurl: "https://hooks.slack.com/services/xxx/xxx/xxx"
 #通知するアドレス
 slackchannel: "#bot-notification"
 slackusername: "tftpsan"
nodes:
 # ノードのリスト
 - name: "crs1k-1" # 対象のホスト名
   type: "iosxe" # OS
   spawn: "telnet 192.168.196.100" # loginするコマンド
   loginuser: "name" # login name
   loginpass: "pass" # login pass
   enablepass: "pass" # enable pass
 - name: "crs1k-1-clone"
   type: "iosxe"
   spawn: "telnet 192.168.196.100"
   loginuser: "name"
   loginpass: "pass"
```
