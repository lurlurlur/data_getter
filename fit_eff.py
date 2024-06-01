import analyze_p as ap
import numpy as np
import os
import sys
from scipy.optimize import curve_fit

if len(sys.argv) != 3:
    print("Usage : python3 get_ovsums.py <mode> <number of algorithms>")
    exit()
mode = int(sys.argv[1])
nalgos = int(sys.argv[2])

def init_fitres(nt, *argv):
    syssize = int(nt.l) + int(nt.L) 
    resdict = dict()
    for i in range(syssize - 4):
        resdict[i] = []
    return resdict 

def linear(X, a, b):
    return -a * X + b

def update_fitres(resdict, dname, nt):
    syssize = int(nt.l) + int(nt.L) 
    a = nt.a
    eff_fname = f'{dname}/eff_ints_a{a}'
    if not os.path.isfile(eff_fname):
        return resdict
    eff_ints = ap.read_file_2d(eff_fname)
    for i in range(syssize - 4):
        eff_ith = eff_ints[i][i+1:]
        Y = np.log(eff_ith)
        X = np.arange(Y.shape[0])
        (a, b), _ = curve_fit(linear, X, Y)

        Y_avg = np.mean(Y)
        ss_tot = np.sum((Y - Y_avg) ** 2)

        Y_fit = linear(X, a, b)
        ss_res = np.sum((Y - Y_fit) ** 2)

        r2 = 1 - (ss_res / ss_tot)
        resdict[i].append([a, r2])
    return resdict

def make_fname(nt, argnames, s):
    fname = f'../p{mode}_result/efffitres/efffitres'
    for n in argnames:
        attr = getattr(nt, n)
        fname += f'_{n}{float(attr)}' if n in ap.float_args else f'_{n}{int(attr)}'
    return fname + f'_s{s}'

def check_exist(nt, argnames):
        return os.path.isfile(make_fname(nt, argnames, 0))

def save_fitres(resdict, nt, argnames):
    syssize = int(nt.l) + int(nt.L)
    for i in range(syssize - 4):
        fname = make_fname(nt, argnames, i)
        print(fname)
        ap.save_2d_lst(fname, resdict[i])
    del resdict
    return None

ap.get_qtt_dict(mode, init_fitres, update_fitres, save_fitres, check_exist, nalgos)
