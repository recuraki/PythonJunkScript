#!/usr/bin/python
# -*- coding: utf-8 -*-


import random
count_lines, count_per_line, count_per_sent = 5,5,5

for l in range(count_lines):
    for s in range(count_per_line):
        st = ""
        for c in range(count_per_sent):
            st = st + chr(random.randint(0x41, 0x5a))
        print st + " ",
    print ""

