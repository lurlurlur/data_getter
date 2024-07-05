home_dir = "/home/gykim"
data_dir = "$(home_dir)/liom/data"
fs_calc_dir = "$(home_dir)/liom/edv2_make/peng_fs_actual"

function main()

	nthr = Threads.nthreads()
	niter = parse(Int64, ARGS[1])
	anum = parse(Int64, ARGS[2])
	size_configs = [(4, 4, 4)]
	ws = [0.2]
	Ws = [3.0, 4, 5, 6, 7, 8, 9, 10, 12.0, 15.0, 18.0, 21.0, 25.0, 30.0]

	for sconf in size_configs
		L, l, M = sconf
		for W in Ws
			for w in ws
				dis_dir = "$(data_dir)/p7_l$(l)_w$(w)_L$(L)_M$(M)_W$(W)"
				syssize = L + l + M
				println(dis_dir)

				Threads.@threads for i=1:nthr*niter
					result_dir = "$(dis_dir)/r$(i)"

					f = open("$(result_dir)/disorder", "r")
					disorder = readlines(f)
					ssite, esite = L + l, syssize - 1
					cmd = `$(fs_calc_dir) $(length(disorder)) $disorder $(result_dir) $(anum) $(ssite) $(esite)`
					run(cmd)
					println("Completed for r=$(result_dir)")
				end
			end
		end
	end
end

if length(ARGS) != 2
	println("Usage : julia --threads <# of threads> calc_fs_7.jl <# of iterations> <anum>")
	exit(1)
end
main()
