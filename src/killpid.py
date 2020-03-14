# -*- encoding: utf-8 -*-
"""
@File    : 
@Time    : 
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 
"""

import os
import signal
import sys
import time
 
time.sleep(1)
 
def kill(pid):
    try:
        a = os.kill(pid, signal.SIGKILL)
        print('kill pid = %s' % (pid))
    except OSError:
        #print(' no pid !!!')
        pass

def kill_all():
    out=os.popen("ps aux | grep digitaltwin").read()
    #print(out)
    #print('---------------')
    for line in out.splitlines():
        #print('cur line == ', line)
        if 'digitaltwin' in line:
            pid = int(line.split()[1])
            #print('cur pid == ', pid)
            kill(pid)

# 确保杀死运行的进程 
kill_all()

