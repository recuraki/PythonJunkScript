import yaml
from copy import deepcopy
import logging
logging.basicConfig(level=logging.DEBUG)
import re

class ruleLoader(object):
    def __init__(self):
        self.rules = dict()


    def load(self, filename):
        with open(filename) as fd:
            buf = yaml.load(fd, Loader=yaml.FullLoader)
            for rule in buf["rules"]:
                mergerule = []
                if "name" not in rule:
                    continue
                rulename = rule["name"]
                if "preinclude" in rule:
                    for preincludename in rule["preinclude"]:
                        if preincludename not in self.rules:
                            logging.warning("not exist such as ", preincludename)
                            continue
                        mergerule.extend(self.rules[preincludename])
                if "rule" in rule:
                    for inputstatement in rule["rule"]:
                        if not all([x in inputstatement for x in ["desc", "action", "re"]]):
                            logging.warning("invalid rule", inputstatement)
                            continue
                        if type(inputstatement["re"]) == str:
                            desc, action, restr = inputstatement["desc"], inputstatement["action"], inputstatement["re"]
                            if re.compile(restr) == None:
                                logging.warning("re error pat:", restr)
                            mergerule.append((desc, action, restr))
                        elif type(inputstatement["re"]) == list:
                            for restr in inputstatement["re"]:
                                if re.compile(restr) == None:
                                    logging.warning("re error pat:", restr)
                                mergerule.append((desc, action, restr))

                self.rules[rulename] = mergerule




if __name__ == "__main__":
    r = ruleLoader()
    r.load("sample.yaml")
    from pprint import pprint
    pprint(r.rules)