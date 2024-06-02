import analyze_p as ap
import os
import sys
import numpy as np

if len(sys.argv) != 4:
    print("Usage : python3 get_vs.py <mode> <number of algorithms> <nsites>")
    exit()

mode = int(sys.argv[1])
nalgos = int(sys.argv[2])
nsites = int(sys.argv[3])
NE = 30

def make_fname(nt, argnames):
    fname = f'../p{mode}_result/isp/isp_agr'
    for n in argnames:
        attr = getattr(nt, n)
        fname += f'_{n}{float(attr)}' if n in ap.float_args else f'_{n}{int(attr)}'
    return fname + f'_n{nsites}'

def check_exist(nt, argnames):
    global calc_mode
    return os.path.isfile(make_fname(nt, argnames))

def init_agr(nt, *argv):
    syssize = int(nt.l) + int(nt.L)
    lst = []
    return lst

def update_agr(qlst, dname, nt):
    fname = f'{dname}/int_spc_a{nt.a}_n{nsites}'
    if not os.path.isfile(fname):
        return qlst
    isparr = np.array(ap.read_file(fname))
    ci = isparr.shape[0] // 2
    cs1 = isparr[(ci-NE//2):(ci+NE//2)]
    cs2 = isparr[(ci-NE//2-1):(ci+NE//2-1)]
    gaps = cs1 - cs2
    for i in range(gaps.shape[0]-1):
        b, s = max(gaps[i], gaps[i+1]), min(gaps[i], gaps[i+1])
        qlst.append(s / b)
    return qlst

def save_agr(qlst, nt, *argv):
    if not qlst:
        return None
    agr = sum(qlst) / len(qlst)
    fname = make_fname(nt, ap.Argnames)
    print(f'{fname} : {agr}')
    ap.save_lst(fname, [agr])
    del qlst
    return None

ap.get_qtt_dict(mode, init_agr, update_agr, save_agr, check_exist, nalgos)
