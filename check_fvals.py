import analyze_p as ap
import os

fresult_dir = '../edv2_make/result2'

for fname in os.listdir(fresult_dir):
    if fname[:8] == 'f_vals_a':
        full_fname_noop = f'{fresult_dir}/{fname}'
        full_fname_op = f'{fresult_dir}/{fname[:6]}_optimized_{fname[7:]}'

        noop_data = ap.read_file(full_fname_noop)
        op_data = ap.read_file(full_fname_op)

        for i in range(800):
            if noop_data[i] != op_data[i]:
                print(f"Error in {i}th row of {full_fname_noop} : {noop_data[i]}, {op_data[i]}")
