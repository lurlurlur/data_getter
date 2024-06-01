import os
import analyze_p as ap

dname = '../p4_result/efffitres'
for fname in os.listdir(f'{dname}/before'):
    b_data = ap.read_file_2d(f'{dname}/before/{fname}')
    data = ap.read_file_2d(f'{dname}/{fname}')
    
    for l in b_data:
        if l not in data:
            print(f'{l} not in new file')
            raise
    print(f'{fname} completed')
