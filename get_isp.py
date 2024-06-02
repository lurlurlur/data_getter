import analyze_p as ap
import os
import sys
import numpy as np

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage : python3 get_medabstisj.py <mode> <number of algorithms> <nsites>")
        exit()
    mode = int(sys.argv[1])
    nalgos = int(sys.argv[2])
    nsites = int(sys.argv[3])

def init_lst(*argv):
    return []

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
    int_spc_sorted = np.sort(int_spc)
    ap.save_lst(fname_isp, int_spc_sorted)

    #spec_fname = '../edv2_make/xxz_spectrum_from_realiz_actual'
    #dis_fname = f'{dname}/disorder'
    #disorder = ap.read_file(dis_fname)

    #cmd = f'{spec_fname} {syssize}'
    #for i in range(syssize):
    #    cmd += f' {disorder[i]}'
    #cmd += f' {dname}/spectrum'
    #os.system(cmd)
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

qtts = ap.get_qtt_dict(mode, init_lst, update_lst, fprocess, check_exist, nalgos)
