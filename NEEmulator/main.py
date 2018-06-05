#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

#sudo pip3 install aiohttp
# pip3 install PyYAML

import sys
import asyncio
from aiohttp import web
import NEEWeb

MGMTPort = 1081



##########################################################
if __name__ == "__main__":
    # グローバルなループイベントの作成
    loop = asyncio.get_event_loop()

    # NEWebの実体化
    runner = web.AppRunner(NEEWeb.app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, port=MGMTPort)

    cors = NEEWeb.registTask(site, loop)

    print("aa")

    # infinity loop!
    res = loop.run_until_complete(asyncio.gather(*cors))
    loop.run_forever()

