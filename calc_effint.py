import analyze_p as ap
import os
import sys
import numpy as np

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage : python3 get_medabstisj.py <mode> <number of algorithms>")
        exit()
    mode = int(sys.argv[1])
    nalgos = int(sys.argv[2])


def to_bin(n):
    bin_rep = bin(n)[2:]
    b_len = len(bin_rep)
    return [i for i in range(b_len) if bin_rep[-i-1] == '1']


def init_lst(*argv):
    return []

def get_coeffs(fname_v, syssize):
    v_vals = ap.read_file(fname_v)

    coeffs = np.zeros((1 << syssize, syssize, syssize))
    for i, v in enumerate(v_vals):
        v_coef = to_bin(i + 1)
        minn, maxx = v_coef[0], v_coef[-1]
        for j in range(1 << syssize):
            dn_sites = to_bin(j)
            do_minus = len([x for x in dn_sites if x in v_coef]) % 2
            coeffs[j, minn, maxx] += v if do_minus == 0 else -v
    return coeffs

def get_norms_1(coeffs, syssize):
    sums = np.sum(coeffs ** 2, axis=0) / (1 << syssize)
    return np.sqrt(sums)

def get_norms_2(fname_v, syssize):
    v_vals = ap.read_file(fname_v)
    v_dict = dict()
    norms = np.zeros((syssize, syssize))

    # initialize
    for i in range(syssize):
        for j in range(i, syssize):
            v_dict[(i, j)] = []

    for i, v in enumerate(v_vals):
        v_coef = to_bin(i + 1)
        minn, maxx = v_coef[0], v_coef[-1]
        #print(f'i = {i}, ({minn}, {maxx})')
        v_dict[(minn, maxx)].append(v ** 2)

    for i in range(syssize):
        for j in range(i, syssize):
            vs = v_dict[(i, j)]
            #print(f'({i}, {j})')
            #print(vs)
            norms[i, j] = np.sqrt(sum(vs))

    return norms

def update_lst(qlst, dname, nt):
    print(dname)
    syssize = int(nt.l) + int(nt.L)
    a = nt.a
    fname_eff = f'{dname}/eff_ints_a{a}'
    if os.path.isfile(fname_eff):
        return qlst
    fname_v = f'{dname}/v_vals_a{a}'
    if not os.path.isfile(fname_v):
        return qlst

    norms_2 = get_norms_2(fname_v, syssize)

    ap.save_2d_lst(fname_eff, norms_2)
    return qlst

def check_exist(nt, argnames):
    return os.path.isfile(make_fname(nt, argnames))

def make_fname(nt, argnames):
    fname = f'../p{mode}_result/efffitres/efffitres'
    for n in argnames:
        attr = getattr(nt, n)
        fname += f'_{n}{float(attr)}' if n in ap.float_args else f'_{n}{int(attr)}'
    return fname

def fprocess(qlst, *argv):
    return qlst


qtts = ap.get_qtt_dict(mode, init_lst, update_lst, fprocess, check_exist, nalgos)
