#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import yaml
from pprint import pprint

TestServerYaml="""
local:
 host: "cisco1"
 ipaddrlo0: "192.168.255.1"

patterns:
  - pattern: "hoge"
    res:
     -
       - aaa
       - bbb
  - pattern: "hostname"
    res:
     -
       - "%{host}s"
  - pattern: "show version"
    res:
     -
       - "%{host}s"
"""

pprint(yaml.load(TestServerYaml))

if __name__ == "__main__":
  cfg = yaml.load(TestServerYaml)
  val = cfg.get("local", {})
  pprint(val)

