#!/usr/local/bin/python

import psutil

import socket
import psutil
import re
import datetime
import time

itProcessList = psutil.process_iter()
for obProcess in itProcessList:
    stProcName = obProcess.name

