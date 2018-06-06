
import asyncio

class notFoundCmd(Exception):
    pass

class CmdEngine(object):

    is_debug :bool
    argparams :dict
    localparams :dict

    def __init__(self, debug = False):
        self.is_debug = debug

    def run(self, actions:list[dict], argparams:dict={}, localparams:dict={}):
        print("CmdEngine.run(): start")
        for action in actions:
            if not "cmd" in action:
                raise notFoundCmd
            cmd:str = action.get("cmd")
            if cmd == "print":

    async def cmd_print(self, params):
        pass

    def cmd_tftpput(self, params):
        pprint("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!NO IMPL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def cmd_httpget(self, params):
        pprint("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!NO IMPL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    async def cmd_wait(self, params):
        pprint("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!NO IMPL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        await asyncio.sleep(1)


