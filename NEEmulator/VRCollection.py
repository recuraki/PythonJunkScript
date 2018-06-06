import asyncio
from aiohttp import web
from pprint import pprint
from VR import VR

##########################################################
### vrdの外側。各インスタンス
##########################################################
class VRd():
    prompt = ""
    host = ""
    is_disconnect = lambda x: x == b""
    loop = ""
    port = 0
    vr: VR = None


    def __init__(self, loop, host="127.0.0.1"):
        self.host = host
        self.loop = loop

    # tcp serverのdisconnect検知関数
    def is_disconnect(self, x):
        return x == b""

    # 実際に走らせる
    """
    run()はself.VRに仮想ルータとしてのインスタンスを作成し、
    TCP serverの inputに関するイベントハンドラとして、task_echodを指定する
    このため、実際の処理はVRdに着呼し、VRに対してイベントの通知を行う
    
    ただし、VRdはあくまで、telnetd的な処理を行うため、あくまで、
    文字列の受け渡しのみを行う。このため、task_echod()では、文字列を受け取り、
    文字列を返すという処理のみを行う
    """
    def run(self, port, prompt):
        self.prompt = prompt
        self.port = port
        self.vr = VR(debug=True)
        return asyncio.start_server(self.task_echod, self.host, port, loop=self.loop)

    def loadscenario(self, data):
        self.vr.loadscenario(data)

    # ユーザからの入力のハンドリング
    async def task_echod(self, cr, cw):
        print("port {0}: event handler lanched".format(self.port))
        while True:
            l: str = await cr.readline()
            # 入力がNullである＝切断要求の場合
            if self.is_disconnect(l):
                print("".format(self.port, ))
                break
            # 入力が有効な値である場合
            if l:
                l = l.decode('utf-8')
                print("task_echod(): data come[port:{0}]: {1}".format(self.port, l))
                reply: str = self.vr.send(l)
                if reply:
                    # データを書き出す。かつ、
                    # drain: asyncioにおける下層のTCPのIOバッファがフラッシュされるまで待つ
                    cw.write(reply.encode('utf-8'))
                    await cw.drain()
                else:
                    print("task_echod(): NO MATCH".format(self.port, l))


##########################################################
### VRを束ねるコレクション
##########################################################
class vrCollection():
    vrd = {}
    host = ""
    loop = ""

    def __init__(self, loop, host="127.0.0.1"):
        self.host = host
        self.loop = loop

    # portの子供をさがし、いるなら返す(いないならFalse)
    def lookup(self, port) -> VR:
        return self.vrd.get(port, False)

    # portを殺す
    def kill(self, port):
        print("ROUGHHHHHHHHHHHHHHHHHHHHHHHHHHHH Impl")
        vrd[port] = None

    # 現在起動しているポートの一覧
    def portlist(self) -> list:
        r = []
        for vr in self.vrd.keys():
            r.append(vr)
        return r

    # portという名前の子供を作る
    def run(self, port):
        print("echod[{0}] RUN".format(port))
        self.vrd[port] = VRd(self.loop, host=self.host)
        return(self.vrd[port].run(int(port), port))