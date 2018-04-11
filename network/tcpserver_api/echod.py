#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import sys
import asyncio
from aiohttp import web

# tcp serverのdisconnect検知関数
is_disconnect = lambda x: x == b""

# 初期値
HOST = "127.0.0.1"
WEBPORT=1080

##########################################################
### Webサーバを作る
##########################################################
async def web_hello(r):
     return web.Response(text = "Hello, World!")

async def web_getportname(request):
    p = request.match_info["name"]
    e = ec.lookup(p)
    if e == False:
        return web.Response(text = "Resource not found")
    return web.Response(text = "name = " + e.prompt)    

async def web_createport(request):
    p = request.match_info["name"]
    e = ec.lookup(p)
    if e != False:
        return web.Response(text = "Resource Already Exist")
    asyncio.ensure_future(ec.run(p))
    return web.Response(text = "ok")

async def web_getsetportname(request):
    p = request.match_info["name"]
    d = request.match_info.get('desc', "NONE")
    e = ec.lookup(p)
    if e == False:
        return web.Response(text = "Resource not found")
    e.set_prompt(d)
    return web.Response(text = "ok")

app = web.Application()
# HTTPd用のルーティング設定
routes = [
    web.get("/", web_hello),
    web.get("/port/{name}", web_getportname),
    web.get("/port/{name}/create", web_createport),
    web.get("/port/{name}/set/{desc}", web_getsetportname),
]
# その追加
app.add_routes(routes)

##########################################################
### echodを束ねる子
##########################################################
class echodCollection():
    echod = {}
    def __init__(self):
        pass

    # portの子供をさがし、いるなら返す(いないならFalse)
    def lookup(self, port):
        return self.echod.get(port, False)

    # portという名前の子供を作る
    def run(self, port):
        print("echod[{0}] RUN".format(port))
        self.echod[port] = echod()
        return(self.echod[port].run(int(port), port))

##########################################################
### echodたち
##########################################################
class echod():
    prompt = ""
    def __init__(self):
        pass

    # プロンプトの変更
    def set_prompt(self, prompt):
        self.prompt = prompt + "\n"

    # 実際に走らせる
    def run(self, port, prompt):
        self.set_prompt(prompt)
        return asyncio.start_server(self.task_echod, HOST, port, loop=loop)

    # ユーザからの入力のハンドリング
    async def task_echod(self, cr, cw):
        print("come")
        while True:
            l = await cr.readline()
            print("read")
            if is_disconnect(l):
                break
            if l:
                cw.write(self.prompt.encode())
                await cw.drain()


##########################################################
### テストしたコード(loopへのタスクの追加)
##########################################################
async def task_1():
    print("task1")
    asyncio.ensure_future(task_2())

async def task_2():
    print("task2")
    await asyncio.sleep(10)
    print("task2-1")

##########################################################
### futureの作成coroutineたち
##########################################################
def registTask():
    cors = []
    cors.append(task_1()) # テスト用
    cors.append(site.start()) # webサーバ
    cors.append(ec.run("10002")) # echod 10002
    cors.append(ec.run("10003")) # echod 10003
    return(cors)

##########################################################
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner)
    ec = echodCollection()
    cors = registTask()
    res = loop.run_until_complete(asyncio.gather(*cors))
    loop.run_forever()
    
