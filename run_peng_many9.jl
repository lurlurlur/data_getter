include("lurITensorTools.jl")

home_dir = "/home/gykim"
data_dir = "$(home_dir)/liom/data"
peng_dir = "$(home_dir)/liom/edv2_make/peng_tisj_vs3_jz_actual"


function main()
	start_time = time()
	nthr = Threads.nthreads()
	syssize = parse(Int64, ARGS[1])
	niter = parse(Int64, ARGS[2])
	ls = [2, 4, 6]
	ws = [0.2]
	Ws = [2.0, 3.0, 5, 7, 9, 12, 15, 21, 30]
	Jzs = [0.0, 0.1, 0.5, 2.0]

	for l in ls	
		for W in Ws
			for w in ws
				for Jz in Jzs
					dis_dir = "$(data_dir)/p9_l$(l)_w$(w)_L$(syssize-l)_W$(W)_J$(Jz)"
					println(dis_dir)
					(!isdir(dis_dir)) && (mkdir(dis_dir))

					Threads.@threads for i=1:nthr*niter
						result_dir = "$(dis_dir)/r$(i)"
						(!isdir(result_dir)) && (mkdir(result_dir))

						f = open("$(result_dir)/disorder", "w")
						disorder = build_disorder(l, w, syssize-l, W)
						for d in disorder
							println(f, d)
						end
						close(f)

						cmd = `$(peng_dir) $(length(disorder)) $(Jz) $disorder $(result_dir)`
						run(cmd)
					end
				end
			end
		end
	end
	end_time = time()
	println("Elapsed time : $(end_time - start_time)")
end

if length(ARGS) != 2
	println("Usage : julia --threads <# of threads> run_peng_many.jl <L> <# of iterations>")
	exit(1)
end
main()
