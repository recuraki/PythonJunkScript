#!env python
# -*- coding: utf-8 -*-

import sys
import yaml

TestServerYaml="""
- pattern: "hoge"
  res:
   - 
     - aaa
     - bbb
   - 
- pattern: "hostname"
  res:
   -
     - "host"
"""




print(yaml.load(TestServerYaml))
