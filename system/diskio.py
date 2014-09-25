#!/usr/local/bin/python

import psutil

import socket
import psutil
import re
import datetime
import time



class DiskIO(object):
    
    def __init__(self):
        pass

    def get_cur_stat(self):
        itProcessList = psutil.process_iter()
        liProcIO = {}
        for obProcess in itProcessList:
            inPid = obProcess.pid
            stProcName = obProcess.name
            liIOCount = obProcess.get_io_counters()
            inReadCount, inWriteCount, inReadBytes, inWriteBytes = liIOCount
            liProcIO[inPid] = (stProcName, inReadCount, inWriteCount, inReadBytes, inWriteBytes)
        return liProcIO
            
def io_sub(liPrev, liCur):
    for inPid in liCur:
        stProcNamePrev, inReadCountPrev, inWriteCountPrev, inReadBytesPrev, inWriteBytesPrev = liPrev.get(inPid, ("",0,0,0,0))
        stProcNameCur, inReadCountCur, inWriteCountCur, inReadBytesCur, inWriteBytesCur = liCur[inPid]
        #print str(inPid), stProcNameCur, inReadCountCur, inWriteCountCur, inReadBytesCur, inWriteBytesCur
        #print str(inPid), stProcNamePrev, inReadCountPrev, inWriteCountPrev, inReadBytesPrev, inWriteBytesPrev 
        print("Prog[{0}:{1}] Read:{2} Write:{3}".format(
                stProcNameCur,
                str(inPid),
                str(inReadBytesCur - inReadBytesPrev),
                str(inWriteBytesCur - inWriteBytesPrev)
                ))
        
        

if __name__ == "__main__":
    d = DiskIO()
    liPrev = {}
    while True:
        liCur = d.get_cur_stat()
        io_sub(liPrev, liCur)
        liPrev = liCur
        time.sleep(1)
        print("--------------------------------")
    

