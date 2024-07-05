home_dir = "/home/gykim"
data_dir = "$(home_dir)/liom/data"
fs_calc_dir = "$(home_dir)/liom/edv2_make/peng_fs_actual"

function main()

	nthr = Threads.nthreads()
	syssize = parse(Int64, ARGS[1])
	niter = parse(Int64, ARGS[2])
	anum = parse(Int64, ARGS[3])
	ssite = parse(Int64, ARGS[4])
	esite = parse(Int64, ARGS[5])
	ls = [0]
	ws = [0.2]
	Ws = [3.0, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 21, 25, 30]

	for l in ls
		for W in Ws
			for w in ws
				dis_dir = "$(data_dir)/p4_l$(l)_w$(w)_L$(syssize-l)_W$(W)"
				println(dis_dir)

				Threads.@threads for i=1:nthr*niter
					result_dir = "$(dis_dir)/r$(i)"

					f = open("$(result_dir)/disorder", "r")
					disorder = readlines(f)
					cmd = `$(fs_calc_dir) $(length(disorder)) $disorder $(result_dir) $(anum) $(ssite) $(esite)`
					run(cmd)
					println("Completed for r=$(result_dir)")
				end
			end
		end
	end
end

if length(ARGS) != 5
	println("Usage : julia --threads <# of threads> calc_fs.jl <L> <# of iterations> <anum> <ssite> <esite>")
	exit(1)
end
main()
