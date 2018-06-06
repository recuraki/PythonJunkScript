
from pprint import pprint
from copy import deepcopy
import re

class EndOfRule(Exception):
    pass

class PatternNotFound(Exception):
    pass

class Scenario(object):
    rules: list = []
    cursor: int = 0
    currule: dict = {}

    def is_exist_by_id(self, ruleid) -> bool:
        # 指定したidのルールが存在するかを確認する
        # T:見つかった F:見つからない
        self.dp("scenario: is_exist(id = {0})".format(ruleid))
        # idに引っかかるものがあるならTrue
        if not list(filter(lambda x: x["id"] == ruleid, self.rules)) == []:
            return True
        else:
            return False

    def dp(self, log):
        if self.isdebug:
            pprint(log)

    def __init__(self, debug: bool=False):
        self.isdebug = debug

    def reset(self):
        # 初期化
        self.sort()
        self.cursor = 0
        self.nextrule()

    def sort(self):
        # 自分のバッファ内にあるルールを key = idでソートする
        self.dp("scenario: sort()")
        self.rules.sort(key=lambda x: x["id"])

    def nextrule(self):
        # 次のルールを読みに行く
        self.dp("scenario: nextrule()")
        self.cursor = self.cursor + 1
        if len(self.rules) < self.cursor:
            raise EndOfRule
        self.currule = self.rules[self.cursor - 1]
        pprint("set rule seq {0}".format(self.cursor - 1))

    def getcurpattern(self):
        if "pattern" in self.currule:
            return self.currule["pattern"]
        else:
            pprint("PatternNotFound")
            pprint(self.currule)
            raise PatternNotFound

    def send(self, msg: str):
        # このシナリオに対する文字列の評価
        # 期待する文字列であった場合、
        self.dp("Scenario.send(): cur ruleid{0} try-str {1}".format(self.currule["id"], msg))
        args = {}
        m = re.search(self.getcurpattern(), msg)
        # fetchできた場合
        if m:
            # パターン内に含まれる?P<name>を取得したなら、それらをargsに突っ込む
            for x in re.finditer("\?P<([^>]*)>", self.getcurpattern()):
                varname = x.groups()[0]
                args[varname] = m.group(varname)

            # 現在のルールを返す
            # args: マッチした文字列のパターン
            # rule: そのルール自身
            ret = {}
            ret["args"] = deepcopy(args)
            ret["rule"] = deepcopy(self.currule)
            ret["match"] = True

            # ルールがpassした場合、次に進む
            try:
                self.nextrule()
            except EndOfRule:
                pass

            return ret

        # パターンが一致しなかった場合
        else:
            ret = {}
            ret["args"] = {}
            ret["rule"] = deepcopy(self.currule)
            ret["match"] = False
            return ret


    def read(self, scenarios: list):
        # シナリオを読み込ませる
        self.dp("scenario: read()")
        self.rules = deepcopy(scenarios)
        self.reset()


    def add(self, ruleid, rule: dict, override: bool=False):
        # idにルールを追加する
        # return: True:成功, False:失敗(404)
        self.dp("scenario: add(id = {0})".format(ruleid))

        # overrideが設定されている場合、そのルールを削除しようとする
        if override:
            self.delete(ruleid)
        else:
            # override = Falseなら存在チェック
            if self.is_exist_by_id(ruleid):
                self.dp("delete: id is already exist")
                return False

        # シナリオの追加と再整列
        self.rules.append(rule)
        self.reset()

    def delete(self, ruleid):
        # 指定されたidのルールを削除する
        # return: True:成功, False:失敗(404)
        self.dp("scenario: delete(id = {0})".format(ruleid))
        if not self.is_exist_by_id(ruleid):
            self.dp("delete: id not found")
            return False
        # 見つかった場合はそのidを除くrulesに書き換え = 削除
        self.rules = list(filter(lambda x: x["id"] != ruleid, self.rules))
        self.dp("DELETE OK")
        return True

import yaml
testYaml="""
scenario: # 読み込み時にIDでsortされる
  - id: "001"
    # patternでマッチした文字列は辞書としてcmdにmatchで渡される
    pattern: "show bgp neighbor (?P<neighbor>[0-9.]+)"
    printafter: "{host}#" # 実行後に返す文字列(主にプロンプト)
    action:
     - cmd: "print"
       param: # コマンドに渡されるパラメータ
       data: 
        - "1st line {neighbor} establish"
        - "2nd line"
     - cmd: "print"
       param: # コマンドに渡されるパラメータ
        data: 
         - "3rd line"
        
  - id: "010"
    cmd: "tftpput"
    pattern: "copy running tftp://(?P<host>[^/]+)/(?P<path>.*)$"
    param:
      host: "{host}"
      path: "{path}"

  - id: "020"
    cmd: "wait"
    pattern: null # パターンがnullの場合は即時実行
    param: null

  - id: "999"
    cmd: "exit"


"""
if __name__ == "__main__":
    d = yaml.load(testYaml)
    s = Scenario(debug=True)
    s.read(d["scenario"])
    pprint(s.rules)
    s.delete("020")
    pprint(list(s.rules))
    s.delete("020")
    pprint(list(s.rules))
    pprint(s.is_exist_by_id("010"))
    pprint(s.is_exist_by_id("020"))
    pprint(s.send("show bgp neighbor 1.1.1.1"))
    pprint(s.send("show bgp neig"))
    pprint(s.send("show bgp neighbor 1.1.1.1"))
    pprint(s.send("copy running tftp://1.1.1.1/config"))


