import analyze_p as ap
import os
import numpy as np
import sys
from scipy.optimize import curve_fit

if len(sys.argv) != 3:
    print("Usage : python3 get_ovsums.py <mode> <number of algorithms>")
    exit()
mode = int(sys.argv[1])
nalgos = int(sys.argv[2])

def linear(X, a, linv):
    return a - X * linv

def expo(X, a, linv):
    return np.exp(linear(X, a, linv))

def init_loclen(*argv):
    q = dict()
    q['exp'] = []
    q['log_lin'] = []
    return q

def do_calc(l, w, L, W, a):
    if l + L != 12:
        return False
    if w != 0.2:
        return False
    if l != 0:
        return False
    return True

def update_loclen(qdict, dname, l, w, L, W, a):
    if not do_calc(l, w, L, W, a):
        return qdict
    syssize = l + L
    fname = f'{dname}/tisj_a{a}_0'
    if not os.path.isfile(fname):
        print(f'{fname} not exist')
        return qdict
    
    Y = np.abs(ap.read_file(fname))
    if 0 in Y:
        return qdict
    logY = np.log(Y)
    X = list(range(syssize))
    
    (_, log_linv), _ = curve_fit(linear, X, logY)
    (_, exp_linv), _ = curve_fit(expo, X, Y)
    
    qdict['exp'].append(exp_linv)
    qdict['log_lin'].append(log_linv)
    return qdict

def fprocess(qdict, l, w, L, W, a):
    if not do_calc(l, w, L, W, a):
        return
    for k in list(qdict.keys()):
        med_len = np.median(qdict[k])
        fname = make_fname(l, w, L, W, a, k)
        ap.save_lst(fname, [med_len])

def make_fname(l, w, L, W, a, fitm):
    return f'../p{mode}_result/loclen/loclen_l{l}_w{w}_L{L}_W{W}_a{a}_{fitm}'

def check_exist(l, w, L, W, a):
    return os.path.isfile(make_fname(l, w, L, W, a, 'exp'))

qtts = ap.get_qtt_dict(mode, init_loclen, update_loclen, fprocess, check_exist, nalgos) 
