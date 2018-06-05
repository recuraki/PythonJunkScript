
from pprint import pprint
from copy import deepcopy

class Scenario(object):
    rules: list = []

    def dp(self, log):
        if self.isdebug:
            pprint(log)

    def __init__(self, debug: bool=False):
        self.isdebug = debug

    def sort(self):
        self.dp("scenario: sort()")
        self.rules.sort(key=lambda x: x["id"])

    def read(self, scenarios: list):
        self.dp("scenario: read()")
        self.rules = deepcopy(scenarios)
        self.sort()

    def is_exist_by_id(self, ruleid) -> bool:
        # 指定したidのルールが存在するかを確認する
        # T:見つかった F:見つからない
        self.dp("scenario: is_exist(id = {0})".format(ruleid))
        # idに引っかかるものがあるならTrue
        if not list(filter(lambda x: x["id"] == ruleid, self.rules)) == []:
            return True
        else:
            return False

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

    def add(self, ruleid, scenario: dict, override: bool=False):
        pass


import yaml
testYaml="""
scenario: # 読み込み時にIDでsortされる
  - id: "001"
    cmd: "print"
    # patternでマッチした文字列は辞書としてcmdにmatchで渡される
    pattern: "show bgp neighbor (?P<neighbor>[0-9.]+)"
    printafter: "{host}#" # 実行後に返す文字列(主にプロンプト)
    # > globalで書いちゃっていいかも
    param: # コマンドに渡されるパラメータ
     data: 
       - "{neighbor} establish"
       - "{neighbor} establish"
  - id: "010"
    cmd: "tftpput"
    pattern: "copy running tftp://(?P<host>[^/]+)/(?P<path>.*)$"
    param:
      host: "{host}"
      path: "{path}"

  - id: "999"
    cmd: "exit"

  - id: "020"
    cmd: "wait"
    pattern: null # パターンがnullの場合は即時実行
    param: null

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
