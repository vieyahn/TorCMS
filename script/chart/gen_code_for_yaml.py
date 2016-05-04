# -*- coding: utf-8 -*-

import os
import sys
import random
inws = r'E:\opt\chart'


def get_uu4d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    slice = random.sample(sel_arr, 4)
    return (''.join(slice))


current_arr  = []
for wroot, wdirs, wfiles in os.walk(inws):
    for wfile in wfiles:
        (qian, hou) = os.path.splitext(wfile)
        if hou == '.yaml':
            pass
        else:
            continue
        # print(wfile)
        bb = qian.split('_')
        if len(bb[-1]) == 4:
            current_arr.append(bb[-1])


for wroot, wdirs, wfiles in os.walk(inws):
    for wfile in wfiles:
        (qian, hou) = os.path.splitext(wfile)
        if hou == '.yaml':
            pass
        else:
            continue
        print(wfile)
        bb = qian.split('_')
        if len(bb[-1]) == 4:
            # current_arr.append(bb[-1])
            pass
        else:
            new_sig = get_uu4d()
            while new_sig in current_arr:
                new_sig = get_uu4d()
            old_file = os.path.join(wroot, wfile)
            new_file = os.path.join(wroot, qian + '_' + new_sig + hou)
            current_arr.append(new_sig)

            os.rename(old_file, new_file)
            print(new_file)
