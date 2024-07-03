import numpy as np
import os
import copy
import time
from collections import namedtuple

float_args = ['w', 'W', 'm', 'i']
rng = np.random.default_rng(int((time.time() * 10000) % 10000))

Argtype = None
Argnames = None

def read_file(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
    return [float(l.strip()) for l in lines]

def read_file_2d(fname):
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
    return [[float(x) for x in l.split('\t')] for l in lines]

def save_lst(fname, lst):
    with open(fname, 'w') as f:
        for line in lst:
            f.write(f'{str(line)}\n')

def save_2d_lst(fname, lst_2d):
    new_lines = []
    for line in lst_2d:
        line_str = [str(x) for x in line]
        new_lines.append('\t'.join(line_str))
    save_lst(fname, new_lines)


def get_range(n):
    r = 0
    while n % 2 == 0:
        n = n >> 1
    while n != 0:
        n = n // 2
        r += 1
    return r

def read_file_line(fname, l):
    return read_file(fname)[l]

def get_mode(dname):
    u1 = dname.find('_')
    return dname[1:u1]

def parse_dir(dname):
    us = []
    i = -1
    while True:
        i = dname.find('_', i + 1)
        if i < 0:
            break
        us.append(i)
    strs = [dname[1]]
    argnames = []
    for i, u in enumerate(us):
        argnames.append(dname[u + 1])
        if i < len(us) - 1:
            nxt = us[i + 1]
            strs.append(dname[u+2:nxt])
        else:
            strs.append(dname[u+2:])

    argnames.append('a')
    global Argtype, Argnames
    if Argtype is None:
        Argtype = namedtuple('Argtype', argnames)
    if Argnames is None:
        Argnames = copy.deepcopy(argnames)

    temp_dict = {}
    for i, an in enumerate(argnames[:-1]):
        temp_dict[an] = strs[i + 1]
    return temp_dict

def find_dirs(mode):
    dirs = []
    for dname in os.listdir('../data'):
        if dname[0] == 'p' and dname[-1] != 'p':
            m = get_mode(dname)
            if m == str(mode):
                dirs.append(dname)
    return dirs

def get_qtt_dict(mode, init_ft, update_ft, process_ft, exist_ft, nalgos, *argv):
    result = dict()
    for d in find_dirs(mode):
        print(d)
        print(parse_dir(d))
        temp_dict = parse_dir(d)
        dname1 = f'../data/{d}'
        global Argtype, Argnames
        for a in range(nalgos):
            temp_dict['a'] = a
            nt = Argtype(**temp_dict)
            if exist_ft(nt, Argnames):
                print(f"Quantity for {d} already calculated")
                continue
            print(nt)
            result[nt] = get_qtts(dname1, init_ft, update_ft, process_ft, nt, *argv)
    return result

def get_qtts(dname, init_ft, update_ft, process_ft, nt, *argv):
    global Argnames
    qtts = init_ft(nt, Argnames)
    rid = 1
    while True:
        dname2 = f'{dname}/r{rid}'
        if not os.path.isdir(dname2):
            print(f"Finished in {dname}. The number of realizations is {rid-1}")
            break
        qtts = update_ft(qtts, dname2, nt, *argv)
        rid += 1
    return process_ft(qtts, nt, Argnames, *argv)

# arr : 1d array-like
def get_se_bootstrap(arr, ft, b):
    global rng
    arr = np.array(arr)
    n = arr.shape[0]
    s1 = np.zeros(arr.shape[1:])
    s2 = np.zeros(arr.shape[1:])
    for i in range(b):
        idx_sample = rng.choice(range(n), n, replace=True)
        sample = arr[idx_sample, ...]
        sample_ft = ft(sample, axis=0)
        s1 += sample_ft
        s2 += sample_ft ** 2

    t1 = s2 / (b - 1)
    t2 = s1 ** 2 / (b * (b - 1))
    return np.sqrt(t1 - t2)
    

if __name__ == '__main__':
    print(find_dirs(2))
