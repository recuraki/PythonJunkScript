#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
itertoolsの修行
"""

import itertools
import string
import string,crypt

"""
リストの中からコンビネーションでとる
"""
itTest = itertools.combinations(string.digits, 2)
for liTest in itTest:
    print liTest

"""
リストから総当たりの組み合わせで2つとる
"""
itTest = itertools.permutations(['qaz','wsx','edc', 'rfv', 'tgb', 'yhn', 'ujm', 'zaq', 'xsw', 'cde', 'vfr', 'bgt', 'nhy', 'mju'],2)
for liTest in itTest:
    print liTest

"""
あとは、
>>> string.punctuation+string.ascii_letters+string.digits
'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
>>> string.ascii_letters+string.digits
'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
とかがとれるので、適宜生成
"""
