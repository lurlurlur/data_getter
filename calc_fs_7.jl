include("lurITensorTools.jl")

home_dir = "/home/gykim"
data_dir = "$(home_dir)/liom/data"
ed_dir = "$(home_dir)/liom/edv2_make"

function main()
	nthr = Threads.nthreads()
	niter = parse(Int64, ARGS[1])
	anum = parse(Int64, ARGS[2])
	makenew = parse(Int64, ARGS[3])
	start = parse(Int64, ARGS[4])
	size_configs = [(3, 6, 3)]
	ws = [0.2]
	Ws = [3.0, 4, 5, 6, 7, 8, 9, 10, 12.0, 15.0, 18.0, 21.0, 25.0, 30.0]

	for sconf in size_configs
		L, l, M = sconf
		for W in Ws
			for w in ws
				dis_dir = "$(data_dir)/p7_l$(l)_w$(w)_L$(L)_M$(M)_W$(W)"
				(!isdir(dis_dir)) && (mkdir(dis_dir))
				syssize = L + l + M
				println(dis_dir)

				Threads.@threads for i=start+1:start+nthr*niter
					result_dir = "$(dis_dir)/r$(i)"
					(!isdir(result_dir)) && (mkdir(result_dir))

					if makenew == 1
						f = open("$(result_dir)/disorder", "w")
						fs_calc_dir = "$(ed_dir)/peng_tvf_actual"
						disorder = build_disorder(l, w, L, M, W)
						for d in disorder
							println(f, d)
						end
					else
						f = open("$(result_dir)/disorder", "r")
						fs_calc_dir = "$(ed_dir)/peng_fs_actual"
						disorder = readlines(f)
					end
					ssite, esite = L + l, syssize - 1
					cmd = `$(fs_calc_dir) $(length(disorder)) $disorder $(result_dir) $(anum) $(ssite) $(esite)`
					run(cmd)
					println("Completed for r=$(result_dir)")
				end
			end
		end
	end
end

if length(ARGS) != 3
	println("Usage : julia --threads <# of threads> calc_fs_7.jl <# of iterations> <anum> <new?1:0> <start>")
	exit(1)
end
main()
