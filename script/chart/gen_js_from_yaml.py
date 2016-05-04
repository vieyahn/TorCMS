
# -*- coding: utf-8 -*-

import os
import sys
import random
import yaml
inws = '/opt/chart'


def get_uu4d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    slice = random.sample(sel_arr, 4)
    return (''.join(slice))

raw_cnts = open('tmpl.js').read()

current_arr  = []
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
            sig = bb[-1]
            outfile = './out/j{0}.js'.format(sig)
            fo = open(outfile, 'w')

            infile = os.path.join(wroot, wfile)
            # print(infile)

            yaml_obj = yaml.load(open(infile).read())
            data_dic = yaml_obj['data']
            out_str = []
            for kye in data_dic.keys():
                out_str.append('s{0}:"{1}"'.format( kye, data_dic[kye]))
            data_ut_str = ','.join(out_str)
            stitle = yaml_obj['meta']['title']
            sunit = yaml_obj['meta']['unit']

            u1 = yaml_obj['range']['a1']
            u2 = yaml_obj['range']['a2']
            u3 = yaml_obj['range']['a3']
            u4 = yaml_obj['range']['a4']
            u5 = yaml_obj['range']['a5']
            u6 = yaml_obj['range']['a6']
            u7 = yaml_obj['range']['a7']
            u8   = yaml_obj['range']['a8']
            res_str = raw_cnts.format(data_ut_str, stitle, sunit, u1, u2, u3, u4, u5, u6, u7, u8)
            fo.write(res_str)
            fo.close()