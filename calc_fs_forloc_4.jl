include("lurITensorTools.jl")

home_dir = "/home/gykim"
data_dir = "$(home_dir)/liom/data"
ed_dir = "$(home_dir)/liom/edv2_make"

function main()

	nthr = Threads.nthreads()
	syssize = parse(Int64, ARGS[1])
	niter = parse(Int64, ARGS[2])
	anum = parse(Int64, ARGS[3])
	makenew = parse(Int64, ARGS[4]) # new : 1, use original : 0
	start = parse(Int64, ARGS[5]) 
	ssite = parse(Int64, ARGS[6])
	esite = parse(Int64, ARGS[7])
	cssite = parse(Int64, ARGS[8])
	ls = [0, 4]
	ws = [0.2]
	Ws = [3.0, 4, 5, 6, 7, 8, 9, 10, 12.0, 15.0, 18.0, 21, 25, 30]

	for l in ls
		for W in Ws
			for w in ws
				dis_dir = "$(data_dir)/p4_l$(l)_w$(w)_L$(syssize-l)_W$(W)"
				println(dis_dir)
				(!isdir(dis_dir)) && (mkdir(dis_dir))

				Threads.@threads for i=start+1:start+nthr*niter
					result_dir = "$(dis_dir)/r$(i)"
					(!isdir(result_dir)) && (mkdir(result_dir))

					if makenew == 1
						f = open("$(result_dir)/disorder", "w")
						fs_calc_dir = "$(ed_dir)/peng_tvf_actual"
						disorder = build_disorder(l, w, syssize-l, W)
						for d in disorder
							println(f, d)
						end
					else
						f = open("$(result_dir)/disorder", "r")
						fs_calc_dir = "$(ed_dir)/peng_fs_actual"
						disorder = readlines(f)
					end
					close(f)
					cmd = `$(fs_calc_dir) $(length(disorder)) $disorder $(result_dir) $(anum) $(ssite) $(esite) $(cssite)`
					run(cmd)
					println("Completed for $(result_dir)")
				end
			end
		end
	end
end

if length(ARGS) != 8
	println("Usage : julia --threads <# of threads> calc_fs.jl <L> <# of iterations> <anum> <new?1:0> <index start> <ssite> <esite> <calc start site>")
	exit(1)
end
main()
