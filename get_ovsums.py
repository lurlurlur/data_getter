import analyze_p as ap
import pickle
import os
import numpy as np
import sys

if len(sys.argv) != 3:
    print("Usage : python3 get_ovsums.py <mode> <number of algorithms>")
    exit()
mode = int(sys.argv[1])
nalgos = int(sys.argv[2])

def init_ovsum(*argv):
    return []

def update_ovsum(qlst, dname, nt):
    syssize = int(nt.l) + int(nt.L)
    ovsum = 0
    f0 = f'{dname}/tisj_a{nt.a}_0'
    if not os.path.isfile(f0):
        print(f'{f0} not exist')
        return qlst
    for i in range(syssize):
        fname = f'{dname}/tisj_a{nt.a}_{i}'
        ovsum += ap.read_file_line(fname, i)
    qlst.append(ovsum)
    return qlst

def make_fname(nt, argnames):
    fname = f'../p{mode}_result/ovsum/ovsum'
    for n in argnames:
        attr = getattr(nt, n)
        fname += f'_{n}{float(attr)}' if n in ap.float_args else f'_{n}{int(attr)}'
    return fname

def check_exist(nt, argnames):
    return os.path.isfile(make_fname(nt, argnames))

def fprocess(qlst, *argv):
    return qlst

qtts = ap.get_qtt_dict(mode, init_ovsum, update_ovsum, fprocess, check_exist, nalgos)
keys = qtts.keys()
meds_dict = dict()
for k in keys:
    print(k)
    qlst = qtts[k]
    med_val = [np.median(qlst)]
    fname = make_fname(k, ap.Argnames)
    ap.save_lst(fname, med_val)
