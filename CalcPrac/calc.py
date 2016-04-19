#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

t = 0

for i in range(1,10):
    c = random.randint(100,1000)
    t = t + c
    print("%12ls" % str(c))

print("%12ls" % t)

