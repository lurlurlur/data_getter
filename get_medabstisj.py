import analyze_p as ap 
import os
import sys
import numpy as np

if len(sys.argv) != 4:
    print("Usage : python3 get_medabstisj.py <mode> <number of algorithms> <calc_mode>")
    exit()
mode = int(sys.argv[1])
nalgos = int(sys.argv[2])
# calc_mode 0 : median, 1 : standard error of median
calc_mode = int(sys.argv[3])

def init_lst(*argv):
    return []

def update_lst(qlst, dname, nt):
    syssize = int(nt.l) + int(nt.L)
    a = nt.a
    f0 = f'{dname}/tisj_a{a}_0'
    if not os.path.isfile(f0):
        #print(f'{f0} not exist')
        return qlst
    all_tisjs = []
    for i in range(syssize):
        fname = f'{dname}/tisj_a{a}_{i}'
        tisjs = ap.read_file(fname)
        atisjs = [abs(x) for x in tisjs]
        all_tisjs.append(atisjs)
    qlst.append(all_tisjs)
    return qlst

def check_exist(nt, argnames):
    global calc_mode
    return os.path.isfile(make_fname(nt, argnames, 0, calc_mode))

def make_fname(nt, argnames, s, calc_mode):
    if calc_mode == 0:
        fname = f'../p{mode}_result/matisj/matisj'
    elif calc_mode == 1:
        fname = f'../p{mode}_result/matisj/stderr'
    else:
        print("Bad calc_mode")
        exit()

    for n in argnames:
        attr = getattr(nt, n)
        fname += f'_{n}{float(attr)}' if n in ap.float_args else f'_{n}{int(attr)}'
    return fname + f'_s{s}'

def fprocess_med(qlst, *argv):
    qarr = np.array(qlst)
    medians = np.median(qarr, 0)
    return medians

def fprocess_err(qlst, *argv):
    qarr = np.array(qlst)
    try:
        std_err = ap.get_se_bootstrap(qarr, np.median, 1000)
    except:
        print("Error")
        return None
    return std_err

if calc_mode == 0:
    qtts = ap.get_qtt_dict(mode, init_lst, update_lst, fprocess_med, check_exist, nalgos)
elif calc_mode == 1:
    qtts = ap.get_qtt_dict(mode, init_lst, update_lst, fprocess_err, check_exist, nalgos)

keys = qtts.keys()
for k in keys:
    l, w, L, W, a = k
    syssize = int(l) + int(L)
    qarr = qtts[k]
    for i in range(syssize):
        try:
            lst_to_save = qarr[i]
            fname = make_fname(k, ap.Argnames, i, calc_mode)
            ap.save_lst(fname, lst_to_save)
        except:
            print(f'exception in {k}, {i}')

print(qtts)
