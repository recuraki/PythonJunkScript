import asyncio
from aiohttp import web
from pprint import pprint


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
    def lookup(self, port):
        return self.vrd.get(port, False)

    # 現在起動しているポートの一覧
    def portlist(self):
        r = []
        for vr in self.vrd.keys():
            r.append(vr)
        return r


    # portという名前の子供を作る
    def run(self, port):
        print("echod[{0}] RUN".format(port))
        self.vrd[port] = VRd(self.loop, host=self.host)
        return(self.vrd[port].run(int(port), port))

##########################################################
### vrdの外側。各インスタンス
##########################################################
class VRd():
    prompt = ""
    host = ""
    is_disconnect = lambda x: x == b""
    loop = ""
    port = 0


    def __init__(self, loop, host="127.0.0.1"):
        self.host = host
        self.loop = loop

    # tcp serverのdisconnect検知関数
    def is_disconnect(self, x):
        return x == b""

    # 実際に走らせる
    def run(self, port, prompt):
        self.prompt = prompt
        self.port = port
        return asyncio.start_server(self.task_echod, self.host, port, loop=self.loop)

    # ユーザからの入力のハンドリング
    async def task_echod(self, cr, cw):
        pass
        print("come")
        while True:
            l = await cr.readline()
            print("read")
            if self.is_disconnect(l):
                break
            if l:
                cw.write("test".encode())
                await cw.drain()

