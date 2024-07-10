import analyze_p as ap
import os
import numpy as np
import sys

if len(sys.argv) != 4:
    print("Usage : python3 get_fs.py <mode> <number of algorithms> <median(0)/distribution(1)>")
    exit()
mode = int(sys.argv[1])
nalgos = int(sys.argv[2])
calc_mode = int(sys.argv[3])
if calc_mode not in [0, 1]:
    print(f"Invalid argument: {calc_mode}")
    exit()

def make_fname(nt, argnames):
    if calc_mode == 0:
        fname = f'../p{mode}_result/medeff/medeff'
    elif calc_mode == 1:
        fname = f'../p{mode}_result/meddist/meddist'
    for n in argnames:
        attr = getattr(nt, n)
        fname += f'_{n}{float(attr)}' if n in ap.float_args else f'_{n}{int(attr)}'
    return fname

def check_exist(nt, argnames):
    return os.path.isfile(make_fname(nt, argnames))

def init_medeff(nt, *argv):
    return None

def update_medeff(data, dname, nt):
    syssize = int(nt.l) + int(nt.L)
    fname = f'{dname}/eff_ints_a{nt.a}'
    if not os.path.isfile(fname):
        return data

    effs = np.array(ap.read_file_2d(fname))
    effs_3d = effs[np.newaxis, :, :]
    if data is None:
        return effs_3d
    result = np.concatenate((effs_3d, data))
    return result

def save_medeff(arr, nt, *argv):
    if arr is None:
        return None
    fname = make_fname(nt, ap.Argnames)
    if calc_mode == 0:
        meds = np.median(arr, axis=0)
        ap.save_2d_lst(fname, meds)
    elif calc_mode == 1:
        syssize = int(nt.l) + int(nt.L)
        for i in range(syssize):
            for j in range(i, syssize):
                final_fname = fname + f'_s{i}_e{j}'
                effs = arr[:, i, j]
                ap.save_lst(final_fname, effs)
    del arr
    return None

ap.get_qtt_dict(mode, init_medeff, update_medeff, save_medeff, check_exist, nalgos)
