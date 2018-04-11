TCPソケットサーバを書く練習

要件
-----

port 10000 - 10004 の5つのポートで値を受け取り、それぞれ1lineを受け取り自分のポート番号を返却するものとする

PATCH echo/<port>/msg/<msg> を投げることで、それぞれのポート<port>は<msg>を返すものとする


PUT echo/<port> とすると、新しく、<port>でaの動作をするtcp serverが立ち上がる