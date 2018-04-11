#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import sys
import asyncio
import time
from aiohttp import web

is_disconnect = lambda x: x == b""

HOST = "127.0.0.1"
# WEBPORT=1080

### 適当にWebの処理
async def web_hello(r):
     return web.Response(text = "Hello, World!")
app = web.Application()
routes = [
    web.get("/", web_hello)
]
app.add_routes(routes)


### echodの定義
class echod():
    prompt = ""
    def __init__(self):
        pass
    
    def run(self, port, prompt):
        print("create" + prompt)
        self.prompt = prompt
        return asyncio.start_server(self.task_echod, HOST, port, loop=loop)

    async def task_echod(self, cr, cw):
        print("come")
        while True:
            l = await cr.readline()
            if is_disconnect(l):
                break
            if l:
                cw.write(self.prompt.encode())
                await cw.drain()

# テスト用！
async def task_1():
    print("task1")
    asyncio.ensure_future(task_2())

async def task_2():
    print("task2")
    await asyncio.sleep(10)
    print("task2-1")
                

# futureの登録
def registTask():
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner)
    cors = []
    cors.append(task_1()) # テスト用
    cors.append(site.start()) # webサーバ
    cors.append(echod().run(10002, "port1")) # echod 10002
    cors.append(echod().run(10003, "port2")) # echod 10003
    return(cors)

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    cors = registTask()
    res = loop.run_until_complete(asyncio.gather(*cors))
    #loop.call_soon(task_1)
    loop.run_forever()
    
