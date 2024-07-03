import analyze_p as ap
import os
import sys
import numpy as np

# calc_mode : 0 if get all interaction, 1 if get interaction of LIOMs in MBL region only

if len(sys.argv) != 4:
    print("Usage : python3 get_vs.py <mode> <number of algorithms> <calc_mode>")
    exit()
mode = int(sys.argv[1])
nalgos = int(sys.argv[2])
calc_mode = int(sys.argv[3])

def make_fname(nt, argnames, r, m, check_mode):
    fname = f'../p{mode}_result/vs/'
    if check_mode:
        fname += 'copied/'
    if m == 0:
        fname += 'vs'
    elif m == 1:
        fname += 'vsloc'
    else:
        print('Invalid mode')
        exit(1)
    for n in argnames:
        attr = getattr(nt, n)
        fname += f'_{n}{float(attr)}' if n in ap.float_args else f'_{n}{int(attr)}'
    return fname + f'_r{r}'

def check_exist(nt, argnames):
    global calc_mode
    return os.path.isfile(make_fname(nt, argnames, 1, calc_mode, True))

def init_dict(nt, *argv):
    if 'M' in nt._fields or 'i' in nt._fields:
        syssize = int(nt.l) + int(nt.L) + int(nt.M)
    else:
        syssize = int(nt.l) + int(nt.L)
    d = dict()
    for i in range(1, syssize + 1):
        d[i] = []
    return d

def update_dict(qdict, dname, nt):
    global calc_mode
    if 'M' in nt._fields or 'i' in nt._fields:
        syssize = int(nt.l) + int(nt.L) + int(nt.M)
    else:
        syssize = int(nt.l) + int(nt.L)
    fname = f'{dname}/v_vals_a{nt.a}'
    if not os.path.isfile(fname):
        #print(f'{fname} not exist')
        return qdict
    vs = ap.read_file(fname)
    for n, v in enumerate(vs):
        r = ap.get_range(n + 1)
        if calc_mode == 0:
            qdict[r].append(v)
        elif calc_mode == 1:
            if (n + 1) % (1 << int(nt.l)) == 0:
                qdict[r].append(v)
        else:
            print('Invalid mode')
            exit(1)
    return qdict

def save_vs(qdict, nt, *argv):
    global calc_mode
    if 'M' in nt._fields:
        max_range = int(nt.l) + int(nt.L) + int(nt.M)
    else:
        max_range = int(nt.l) + int(nt.L) if calc_mode == 0 else int(nt.L)

    for r in range(1, max_range + 1):
        fname = make_fname(nt, ap.Argnames, r, calc_mode, False)
        ap.save_lst(fname, qdict[r])
    del qdict
    return None

ap.get_qtt_dict(mode, init_dict, update_dict, save_vs, check_exist, nalgos)
