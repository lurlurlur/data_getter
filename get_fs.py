import analyze_p as ap
import os
import numpy as np
import sys

if len(sys.argv) != 3:
    print("Usage : python3 get_fs.py <mode> <number of algorithms>")
    exit()
mode = int(sys.argv[1])
nalgos = int(sys.argv[2])

def make_fname(nt, argnames, s, d):
    fname = f'../p{mode}_result/fs/fs'
    for n in argnames:
        attr = getattr(nt, n)
        fname += f'_{n}{float(attr)}' if n in ap.float_args else f'_{n}{int(attr)}'
    return fname + f'_s{s}_d{d}'

def check_exist(nt, argnames):
    return os.path.isfile(make_fname(nt, argnames, 0, 0))

def syssize_from_nt(nt):
    if 'M' in nt._fields:
        return int(nt.l) + int(nt.L) + int(nt.M)
    return int(nt.l) + int(nt.L)
    

def init_fs(nt, *argv):
    syssize = syssize_from_nt(nt)
    return np.zeros((800, syssize, syssize))
    
def update_fs(arr, dname, nt):
    syssize = syssize_from_nt(nt)
    for s in range(syssize):
        for d in range(syssize):
            fname = f'{dname}/f_vals_optimized_a{nt.a}_s{s}_d{d}'
            if not os.path.isfile(fname):
                continue
            arr[:, s, d] += np.array(ap.read_file(fname))
    return arr

def save_fs(arr, nt, *argv):
    syssize = syssize_from_nt(nt)
    for s in range(syssize):
        for d in range(syssize):
            hist = arr[:, s, d]
            if np.sum(hist) < 1:
                continue
            fname = make_fname(nt, ap.Argnames, s, d)
            ap.save_lst(fname, hist)
    del arr
    return None

ap.get_qtt_dict(mode, init_fs, update_fs, save_fs, check_exist, nalgos)
