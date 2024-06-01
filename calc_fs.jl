home_dir = "/home/gykim"
data_dir = "$(home_dir)/prx7/data"
fs_calc_dir = "$(home_dir)/prx7/edv2_make/peng_fs_opt10_actual"

function main()

	nthr = Threads.nthreads()
	syssize = parse(Int64, ARGS[1])
	niter = parse(Int64, ARGS[2])
	ls = [4, 6]
	ws = [0.2]
	#Ws = [3.0, 4.0, 5, 6, 8, 10, 15, 21, 25, 30]
	#Ws = [3.3, 3.6, 3.8, 4.2, 4.4, 4.6, 4.8, 5.5, 6.5, 7, 9]
	#Ws = [4.4, 4.6, 4.8, 5, 5.5, 6, 6.5, 7, 8, 9]
	#Ws = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
	#[4.2, 4.4, 4.6, 4.8, 5, 5.5, 6, 6.5, 7, 8, 9, 10, 12, 15, 18, 21, 25, 30]
	#Ws = [3.3, 3, 3.6, 3.8, 4, 4.2, 4.4, 4.6, 4.8, 5, 5.5, 6, 6.5, 7, 8, 9]#, 10, 12, 15, 18, 21, 25, 30]
	Ws = [12.0, 15.0, 18.0, 21.0, 25.0, 30.0]
	#Ws = [10.0]

	for l in ls
		for W in Ws
			for w in ws
				dis_dir = "$(data_dir)/p4_l$(l)_w$(w)_L$(syssize-l)_W$(W)"
				println(dis_dir)

				Threads.@threads for i=1:nthr*niter
					result_dir = "$(dis_dir)/r$(i)"

					f = open("$(result_dir)/disorder", "r")
					disorder = readlines(f)
					cmd = `$(fs_calc_dir) $(length(disorder)) $disorder $(result_dir)`
					run(cmd)
					println("Completed for r=$(result_dir)")
				end
			end
		end
	end
end

if length(ARGS) != 2
	println("Usage : julia --threads <# of threads> calc_fs.jl <L> <# of iterations>")
	exit(1)
end
main()
