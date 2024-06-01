import analyze_p as ap
import os
import sys
import numpy as np

if len(sys.argv) != 3:
    print("Usage : python3 get_ovhist.py <mode> <number of algorithms>")
    exit()

mode = int(sys.argv[1])
nalgos = int(sys.argv[2])

def fname_b(nt, argnames):
    fn = ''
    for n in argnames:
        attr = getattr(nt, n)
        fn += f'_{n}{float(attr)}' if n in ap.float_args else f'_{n}{int(attr)}'
    return fn

def make_fname_bin(nt, argnames, s):
    return f'../p{mode}_result/ovhist/bin{fname_b(nt, argnames)}_s{s}'

def make_fname_h(nt, argnames, s):
    return f'../p{mode}_result/ovhist/h{fname_b(nt, argnames)}_s{s}'

def check_exist(nt, argnames):
    return os.path.isfile(make_fname_bin(nt, argnames, 0))

def init_dict(nt, *argv):
    syssize = int(nt.l) + int(nt.L)
    d = dict()
    for i in range(syssize):
        d[i] = []
    return d

def update_dict(qdict, dname, nt):
    syssize = int(nt.l) + int(nt.L)
    for s in range(syssize):
        ov_fname = f'{dname}/tisj_a{nt.a}_{s}'
        if not os.path.isfile(ov_fname):
            continue
        max_ov = ap.read_file_line(ov_fname, s)
        qdict[s].append(max_ov / (1 << syssize))
    return qdict

def save_ovhist(qdict, nt, *argv):
    syssize = int(nt.l) + int(nt.L)
    bins = np.linspace(0.0, 1.0, 101)
    for s in range(syssize):
        qtts = qdict[s]
        hist, result_bins = np.histogram(qtts, bins)
        fname_bin = make_fname_bin(nt, ap.Argnames, s)
        fname_h = make_fname_h(nt, ap.Argnames, s)
        ap.save_lst(fname_bin, result_bins)
        ap.save_lst(fname_h, hist)
    del qdict
    return None

ap.get_qtt_dict(mode, init_dict, update_dict, save_ovhist, check_exist, nalgos)
