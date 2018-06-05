import sys
import asyncio
from aiohttp import web
import VRCollection
import json
from pprint import pprint
import yaml
from VR import VR


# 初期値
HOST = "127.0.0.1"
WEBPORT = 1080
vrc = None

##########################################################
### Webサーバを作る
##########################################################


# ダミー関数
async def web_hello(request: web.BaseRequest):
     return web.Response(text="Hello, World!")


# 現在 Startしているセッションのリスト
async def web_getportlist(request: web.BaseRequest):
    ports = vrc.portlist()
    return web.json_response(text=json.dumps(ports))


async def web_getdetail(request: web.BaseRequest):
    # 引数の処理
    p = request.match_info["port"]
    print("GET detail [{0}]".format(p))

    # VR Collectionからの検索: 存在しなければNG
    e = vrc.lookup(p)
    if not e:
        return web.Response(text="Resource not found",
                            status=404)

    # 処理
    return web.json_response(text=json.dumps({"name": p}))


async def web_createvr(request: web.BaseRequest):
    # 引数の処理
    p = request.match_info["port"]

    # VR Collectionからの検索: 存在してはならない
    e = vrc.lookup(p)
    if e:
        return web.Response(text="Conflict, Resource Already Exist",
                            status=409)

    # ユーザからのペイロードの判定と読み込み
    data =  await request.read()
    if request.content_type == "application/x-yaml":
        data = yaml.load(data)
    elif request.content_type == "application/json":
        data = json.loads(data)
    else:
        return web.Response(status=400,
                            reason="Invalid Content-Type")

    # 処理
    asyncio.ensure_future(vrc.run(p))
    return web.Response(text="ok")


async def web_putscenario(request: web.BaseRequest):
    # 引数の処理
    p = request.match_info["port"]
    # VR Collectionからの検索: 存在しなければNG
    e = vrc.lookup(p)
    if not e:
        return web.Response(status=404,
                            reason="Resource Not Found")

    # ユーザからのペイロードの判定と読み込み
    data =  await request.read()
    if request.content_type == "application/x-yaml":
        data = yaml.load(data)
    elif request.content_type == "application/json":
        data = json.loads(data)
    else:
        return web.Response(status=400, reason="Invalid Content-Type")

    return web.Response(text=str(data))


async def web_delscenario(request: web.BaseRequest):
    # 引数の処理
    p = request.match_info["port"]
    id = request.match_info["id"]
    print("DELETE SCENARIO [{0}] id: {1}".format(p,id))

    # VR Collectionからの検索: 存在しなければNG
    e = vrc.lookup(p)
    if not e:
        return web.Response(text="Resource not found",
                            status=404)

    e.delscenario(id)

    return web.Response(text="name = " + e.prompt)


async def web_restart(request: web.BaseRequest):
    # 引数の処理
    p = request.match_info["port"]
    print("Request Vitrual Router [port: {0}]".format(p, id))

    # VR Collectionからの検索
    e = vrc.lookup(p)
    if not e:
        return web.Response(text="Resource not found",
                            status=404)

    return web.Response(text="name = " + e.prompt)


async def web_getstatus(request: web.BaseRequest):
    # 引数の処理
    p = request.match_info["port"]
    print("Request Vitrual Router [port: {0}]".format(p, id))

    # VR Collectionからの検索
    e = vrc.lookup(p)
    if not e:
        return web.Response(text="Resource not found",
                            status=404)

    return web.Response(text="name = " + e.prompt)


async def web_createport(request):
    p = request.match_info["port"]
    e = vrc.lookup(p)
    if e:
        return web.Response(text="Resource Already Exist")
    asyncio.ensure_future(vrc.run(p))
    return web.Response(text="ok")


async def web_getsetportname(request):
    p = request.match_info["port"]
    d = request.match_info.get('desc', "NONE")
    e = vrc.lookup(p)
    if not e:
        return web.Response(text="Resource not found")
    e.prompt = d
    return web.Response(text="ok")


def registTask(site, loop):
    global vrc
    cors = []
    vrc = VRCollection.vrCollection(loop, host=HOST)
    cors.append(site.start())  # webサーバ
    return (cors)


app = web.Application()
# HTTPd用のルーティング設定
routes = [
    web.get   ("/", web_hello),
    web.get   ("/vr", web_getportlist),
    web.get   ("/vr/{port}", web_getdetail),
    web.put   ("/vr/{port}", web_createvr),
    web.put   ("/vr/{port}/scenario/{id}", web_putscenario),
    web.delete("/vr/{port}/scenario/{id}", web_delscenario),
    web.post  ("/vr/{port}/restart", web_restart),
    web.get   ("/vr/{port}/status", web_getstatus),

    web.get("/vr/{port}/create", web_createport),
    web.get("/port/{port}/set/{desc}", web_getsetportname),
]
# その追加
app.add_routes(routes)