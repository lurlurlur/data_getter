import calc_effint as ce

fname = '../data/p4_l4_w0.2_L8_W6.0/r1234/v_vals_a1'
norms_2 = ce.get_norms_2(fname, 12)
print(norms_2)
coeffs = ce.get_coeffs(fname, 12)
norms_1 = ce.get_norms_1(coeffs, 12)
print()
print(norms_1)
print()
print(norms_2 - norms_1)
