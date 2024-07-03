import analyze_p as ap
import os
import sys
import numpy as np

def init_lst(*argv):
    return []

def count_ones(n):
    if n == 0:
        return 0
    return count_ones(n >> 1) + (0 if n & 1 == 0 else 1)

def symmetrize(int_spc, nones):
    assert int_spc.shape[0] == 1 << (nones * 2)
    symmed = []
    for i in range(1 << (nones * 2)):
        if count_ones(i) == nones:
            symmed.append(int_spc[i])
    return np.array(symmed)

def modify_spc(int_spc, s):
    assert int_spc.shape[0] == 1 << nsites
    new_spc = np.zeros_like(int_spc)

    for i in range(1 << nsites):
        if i & (1 << s):
            new_spc[i] = int_spc[i - (1 << s)] - int_spc[i]
        else:
            new_spc[i] = int_spc[i] + int_spc[i + (1 << s)]
    return new_spc

def update_lst(qlst, dname, nt):
    syssize = int(nt.l) + int(nt.L)
    if int(nt.l) != 0 and int(nt.L) != nsites:
        return qlst
    if syssize >= 14:
        return qlst
    if syssize < nsites:
        return qlst
    a = nt.a
    fname_isp = f'{dname}/int_spc_a{a}_n{nsites}'
    fullv_fname = f'{dname}/v_vals_a{a}'
    p = 1 << (syssize - nsites)
    v_full = np.zeros(1 << syssize)
    v_full[1:] = ap.read_file(fullv_fname)
    
    int_spc = v_full[::p]
    for s in range(nsites):
        int_spc = modify_spc(int_spc, s)

    if sym != 0:
        fname_isp += '_sym'
        int_spc = symmetrize(int_spc, nsites//2)

    int_spc_sorted = np.sort(int_spc)
    ap.save_lst(fname_isp, int_spc_sorted)


    return qlst

def check_exist(nt, argnames):
    return os.path.isfile(make_fname(nt, argnames))

def make_fname(nt, argnames):
    fname = f'../p{mode}_result/intspc/intspc'
    for n in argnames:
        attr = getattr(nt, n)
        fname += f'_{n}{float(attr)}' if n in ap.float_args else f'_{n}{int(attr)}'
    return fname

def fprocess(qlst, *argv):
    return qlst


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage : python3 get_medabstisj.py <mode> <number of algorithms> <nsites> <sym>")
        exit()
    mode = int(sys.argv[1])
    nalgos = int(sys.argv[2])
    nsites = int(sys.argv[3])
    sym = int(sys.argv[4])

    qtts = ap.get_qtt_dict(mode, init_lst, update_lst, fprocess, check_exist, nalgos)
