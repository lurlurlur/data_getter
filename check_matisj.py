import os
import analyze_p as ap

dname = '../p4_result/matisj'
for fname in os.listdir(f'{dname}/before'):
    b_data = ap.read_file_2d(f'{dname}/before/{fname}')
    data = ap.read_file_2d(f'{dname}/{fname}')
    
    for i, x in enumerate(b_data):
        if data[i] != x:
            print(f'{x} not in new file')
            raise
    print(f'{fname} completed')
