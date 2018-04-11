TCPソケットサーバを書く練習

要件
-----

●起動するとport 10002 - 10003 の2つのポートで値を受け取り、それぞれ1lineを受け取りプロンプトを返却するものとする

●GET /port/{name} を投げることで{name}のポートの現在のプロンプトを返す

●GET /port/{name}/create とすると、新しく、で{name}ポートで待ち受けるtcp serverが立ち上がる

●GET /port/{name}/set/{desc}とすると、{name}のポートのプロンプトが変えられる
