function op_from_mpo(mpo)
	L = length(mpo)
	oper = ITensor(1.0+0*im)
	for i=1:L
		oper *= mpo[i]
	end
	end_plev = 1
	for ind in inds(oper)
		if plev(ind) > 0
			end_plev = plev(ind)
			break	
		end
	end
	return mapprime(oper, end_plev, 1)
end

function mat_from_op(op, sites)
	L = length(sites)
	op_arr = Array(op, sites', sites)
	op_mat = reshape(op_arr, 1<<L, 1<<L)
	return op_mat
end

function build_disorder(L, W)
	disorder = zeros(L)
	for i=1:L
		disorder[i] = (rand() - 0.5) * 2 * W
	end
	return disorder	
end

function build_disorder(l, w, L, W)
	syssize = l + L
	disorder = zeros(syssize)
	for i=1:syssize
		ds = (i > l) ? W : w
		disorder[i] = (rand() - 0.5) * 2 * ds
	end
	return disorder
end

function build_XXZ(sites, L, W; disorder=[], periodic=false)
        ampo = OpSum()
        for j=1:L-1
                ampo += "Sz",j,"Sz",j+1
                ampo += "Sx",j,"Sx",j+1
                ampo += "Sy",j,"Sy",j+1
        end
	if periodic
                ampo += "Sz",L,"Sz",1
                ampo += "Sx",L,"Sx",1
                ampo += "Sy",L,"Sy",1
	end
		
        for j=1:L
		if length(disorder) != L
                	h_j = (rand() - 0.5) * 2 * W
		else
			h_j = disorder[j]
		end
                ampo += h_j,"Sz",j
        end
	return MPO(ampo, sites)
end

function build_XXZ_local(sites, L, W; disorder=[])
	local_terms = Vector{ITensor}(undef, L-1)
	total_ampo = OpSum()
	for i=1:L-1
		ampo = OpSum()
                ampo += "Sz",1,"Sz",2
                ampo += "Sx",1,"Sx",2
                ampo += "Sy",1,"Sy",2
		if length(disorder) != L
			h_i = (rand() - 0.5) * 2 * W
		else
			h_i = disorder[i]
		end
		ampo += h_i,"Sz",1
		if i == L-1
			if length(disorder) != L
				h_L = (rand() - 0.5) * 2 * W
			else
				h_L = disorder[L]
			end
			ampo += h_L,"Sz",2	
		end
		total_ampo += ampo

		act_sites = [sites[i], sites[i+1]]
		local_h_mpo = MPO(ampo, act_sites)
		local_terms[i] = local_h_mpo[1] * local_h_mpo[2]
	end
	return local_terms
end

function mpo_ed_arr(H_mpo, sites)
        Hitensor = op_from_mpo(H_mpo) 
	Hmat = mat_from_op(Hitensor, sites)
        eig_vals = eigvals(Hmat)
        eig_vecs = eigvecs(Hmat)
        return eig_vals, eig_vecs
end


function mpo_ed(H_mpo, sites)
	L = length(H_mpo)
        Hitensor = op_from_mpo(H_mpo)
        Linds = sites'
        Rinds = sites
        eig_vals, eig_vecs = eigen(Hitensor, Linds, Rinds)
	return real([eig_vals[i, i] for i=1:1<<L]), eig_vecs
end

function square_trace(H_mpo)
	L = length(H_mpo)
        tr = ITensor(1.)
        for i=1:L
                tr *= H_mpo[i] * swapprime(dag(H_mpo[i]), 0=>1)
        end
	return scalar(tr)
end


function norm_diag_mat(H_mpo, sites)
	L = length(H_mpo)
        H_full = op_from_mpo(H_mpo, L)
	Hmat = mat_from_op(H_full, L, sites)
        return norm([Hmat[i, i] for i=1:1<<L])^2
end

function my_spectrum_mat(H_mpo, U_mpo, sites)
	L = length(H_mpo)
	H_full = op_from_mpo(H_mpo)
	U_full = op_from_mpo(U_mpo)
	H_mat = mat_from_op(H_full, sites)
	U_mat = mat_from_op(U_full, sites)
	spectrum_mat = adjoint(U_mat) * H_mat * U_mat
	return sort(real([spectrum_mat[i, i] for i=1:1<<L]))
end

function my_spectrum(H_mpo, U_mpo, sites)
	L = length(H_mpo)
	H_full = op_from_mpo(H_mpo)
	U_full = op_from_mpo(U_mpo)
	U_dag = swapprime(dag(U_full''), 2=>3)
	spec_itn = mapprime(U_dag * H_full' * U_full, 3, 1)
	spec_mat = mat_from_op(spec_itn, sites)
	my_spec = real([spec_mat[i, i] for i=1:1<<L])
	sorted = sort(my_spec)
	return my_spec, sorted
end

function no_layer_spec(H_mpo, sites)
	L = length(H_mpo)
	H_full = op_from_mpo(H_mpo)
	H_mat = mat_from_op(H_full, sites)
	return sort(real([H_mat[i, i] for i=1:1<<L]))
end

function overlap_mat(H_mpo, U_mpo, sites, eig_vecs)
	L = length(H_mpo)
	eig_vecs_arr = Array(eig_vecs, sites, inds(eig_vecs)[end])
	eig_vecs_mat = reshape(eig_vecs_arr, 1<<L, 1<<L)
	overlap_vec = zeros(1<<L)
	U_full = op_from_mpo(U_mpo, L)
	U_mat = mat_from_op(U_full, L, sites)
	U_mat_sorted = zeros(ComplexF64, 1<<L, 1<<L)
	
	my_spec = my_spectrum(H_mpo, U_mpo, L, sites)[1]
	spec_ranking = ordinalrank(my_spec)
	for i=1:1<<L
		ranking = spec_ranking[i]
		U_mat_sorted[:, ranking] = U_mat[:, i] end
	
 	for i=1:1<<L
		ith_my_vec = U_mat_sorted[:, i]
		ith_eigvec = eig_vecs_mat[:, i]
		overlap_vec[i] = abs(adjoint(ith_my_vec)*ith_eigvec)
	end
	return overlap_vec, U_mat_sorted
end

function get_qn(num)
	qn = 0
	while num > 0
		qn += num % 2
		num = num >> 1
	end
	return qn
end

function get_qn_dict(qn_dict, num_legs)
	for i=0:num_legs
		qn_dict[i] = []
	end
	for i=1:1<<num_legs
		qnum = get_qn(i-1)
		push!(qn_dict[qnum], i)
	end
	return qn_dict
end

function delta_mpo(L, sites)
 	del_mpo = Vector{ITensor}(undef, L)
	for i=1:L
		del_mpo[i] = delta(sites[i], sites[i]')	
	end
	return del_mpo
end
