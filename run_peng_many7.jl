include("lurITensorTools.jl")

home_dir = "/home/gykim"
data_dir = "$(home_dir)/liom/data"
peng_dir = "$(home_dir)/liom/edv2_make/peng_tisj_vs3_actual"

function main()
	start_time = time()
	nthr = Threads.nthreads()
	niter = parse(Int64, ARGS[1])

	# left(MBL), middle(thermal), right(MBL)
	size_configs = [(5, 4, 3)]
	ws = [0.2]
	Ws = [3.0, 4.0, 5, 6, 7, 8, 9, 10, 12, 15, 18, 21, 25, 30]

	for sconf in size_configs
		L, l, M = sconf
		for W in Ws
			for w in ws
				dis_dir = "$(data_dir)/p7_l$(l)_w$(w)_L$(L)_M$(M)_W$(W)"
				println(dis_dir)
				(!isdir(dis_dir)) && (mkdir(dis_dir))

				Threads.@threads for i=1:nthr*niter
					result_dir = "$(dis_dir)/r$(i)"
					(!isdir(result_dir)) && (mkdir(result_dir))

					try
						f = open("$(result_dir)/disorder", "w")
						disorder = build_disorder(l, w, L, M, W)
						for d in disorder
							println(f, d)
						end
						close(f)

						cmd = `$(peng_dir) $(length(disorder)) $disorder $(result_dir)`
						run(cmd)
					catch
						println("error in $(result_dir)")
					end
				end
			end
		end
	end
	end_time = time()
	println("Elapsed time : $(end_time - start_time)")
end

if length(ARGS) != 1
	println("Usage : julia --threads <# of threads> run_peng_many.jl <# of iterations>")
	exit(1)
end
main()
