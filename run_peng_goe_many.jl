include("lurITensorTools.jl")

home_dir = "/home/gykim"
data_dir = "$(home_dir)/liom/data"
peng_dir = "$(home_dir)/liom/edv2_make/peng_goef_tisj_vs_actual"

function main()
	alpha_dict = Dict()
	alpha_dict[(0.2, 4)] = 0.852
	alpha_dict[(0.2, 6)] = 1.158

	nthr = Threads.nthreads()
	syssize = parse(Int64, ARGS[1])
	mode = parse(Int64, ARGS[2])
	niter = parse(Int64, ARGS[3])
	ls = [6]
	ws = [0.2]
	Ws = [3, 4, 5, 7, 9]
	ms = [0.25, 0.5, 1.0, 2.0, 4.0]

	for l in ls	
		for W in Ws
			for w in ws
				for m in ms
					dis_dir = "$(data_dir)/p$(mode+5)_l$(l)_w$(w)_L$(syssize-l)_W$(W)_m$(m)"
					println(dis_dir)
					(!isdir(dis_dir)) && (mkdir(dis_dir))

					Threads.@threads for i=1:nthr*niter
						result_dir = "$(dis_dir)/r$(i)"
						(!isdir(result_dir)) && (mkdir(result_dir))

						try
							f = open("$(result_dir)/disorder", "w")
							disorder = build_disorder(syssize-l, W)
							for d in disorder
								println(f, d)
							end
							close(f)

							alpha = alpha_dict[(w, l)]
							mfactor = alpha * m / (2 ^ (l / 2))

							cmd = `$(peng_dir) $(l) $(syssize-l) $disorder $(i) 1 $(mfactor) $(result_dir) $(mode)`
							run(cmd)
						catch
							println("error in $(result_dir)")
						end
					end
				end
			end
		end
	end
end

if length(ARGS) != 3
	println("Usage : julia --threads <# of threads> run_peng_many.jl <L> <mode> <# of iterations>")
	println("Mode 0 : full symmetry (do not mix sectors), Mode 1 : no symmetry (mix all sectors)")
	exit(1)
end
main()
