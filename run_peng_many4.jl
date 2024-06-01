include("lurITensorTools.jl")

home_dir = "/home/gykim"
data_dir = "$(home_dir)/liom/data"
peng_dir = "$(home_dir)/liom/edv2_make/peng_tisj_vs3_actual"


function main()
	start_time = time()
	nthr = Threads.nthreads()
	syssize = parse(Int64, ARGS[1])
	niter = parse(Int64, ARGS[2])
	ls = [0]
	ws = [0.2]
	#Ws = [2.0, 2.5]
	#Ws = [3.0, 3.6, 4.4, 4.8, 5.5, 6.5, 7.0, 8.0, 9.0]
	#Ws = [3.0, 3.3, 3.6, 3.8, 4, 4.2, 4.4, 4.6, 4.8, 5, 5.5, 6, 6.5, 7, 8, 9, 10, 12, 15, 18, 21, 25, 30]
	Ws = [8.2, 8.4, 8.6, 8.8, 9.2, 9.4, 9.6, 9.8]
	#Ws = [8.0]

	for l in ls	
		for W in Ws
			for w in ws
				dis_dir = "$(data_dir)/p4_l$(l)_w$(w)_L$(syssize-l)_W$(W)"
				println(dis_dir)
				(!isdir(dis_dir)) && (mkdir(dis_dir))

				Threads.@threads for i=1:nthr*niter
					result_dir = "$(dis_dir)/r$(i)"
					(!isdir(result_dir)) && (mkdir(result_dir))

					try
						f = open("$(result_dir)/disorder", "w")
						disorder = build_disorder(l, w, syssize-l, W)
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

if length(ARGS) != 2
	println("Usage : julia --threads <# of threads> run_peng_many.jl <L> <# of iterations>")
	exit(1)
end
main()
