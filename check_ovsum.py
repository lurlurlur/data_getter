import os
import analyze_p as ap

dname = '../p4_result/ovsum'
for fname in os.listdir(f'{dname}/before'):
    b_data = ap.read_file_2d(f'{dname}/before/{fname}')
    data = ap.read_file_2d(f'{dname}/{fname}')
    
    if b_data[0] != data[0]:
        print(f'{l} not in new file')
        raise
    print(f'{fname} completed')
