using ITensors
using StatsBase
using LinearAlgebra
include("lurITensorTools.jl")

ITensors.disable_warn_order()

function main()
	L = 12 #parse(Int64, ARGS[1])
	w = 0 #parse(Float64, ARGS[2])
	niter = 1 #parse(Int64, ARGS[3])
	sites = siteinds("S=1/2", L)

	spectrum = []

	for i=1:niter
		(i % 10 == 0) && println("$(i)th iter")
		d = build_disorder(L, w)
		H_mpo = build_XXZ(sites, L, 0; disorder=d, periodic=true)
		H_full = op_from_mpo(H_mpo)
		H_mat = mat_from_op(H_full, sites)
		eig_vals = eigvals(H_mat)
		spectrum = vcat(spectrum, eig_vals)
	end

	p95 = StatsBase.percentile(spectrum, 95)
	p5 = StatsBase.percentile(spectrum, 5)
	println("alpha value for N = $(L), w = $(w) is $((p95 - p5) / (2 * sqrt(2)))")
end

if length(ARGS) != 3
	println("Usage : julia get_alpha.jl <L> <w> <# of iterations>")
end
main()
