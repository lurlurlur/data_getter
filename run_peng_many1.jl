include("lurITensorTools.jl")

home_dir = "/home/gykim"
data_dir = "$(home_dir)/liom/data"
peng_dir = "$(home_dir)/liom/edv2_make/peng_tisj_vs3_actual"


function main()
	start_time = time()
	nthr = Threads.nthreads()
	syssize = parse(Int64, ARGS[1])
	niter = parse(Int64, ARGS[2])
	ls = [4]
	ws = [0.2]
	#Ws = [2.0, 2.5]
	#Ws = [3.0, 3.6, 4.4, 4.8, 5.5, 6.5, 7.0, 8.0, 9.0]
	Ws = [3.0, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 21, 25, 30]
	#Ws = [3.0, 3.3, 3.6]
	#Ws = [8.0]

	for l in ls	
		for W in Ws
			for w in ws
				old_dis_dir = "$(data_dir)/p4_l$(0)_w$(w)_L$(syssize)_W$(W)"
				new_dis_dir = "$(data_dir)/p1_l$(l)_w$(w)_L$(syssize-l)_W$(W)"

				(!isdir(old_dis_dir)) && continue
				println(new_dis_dir)
				(!isdir(new_dis_dir)) && (mkdir(new_dis_dir))

				Threads.@threads for i=1:nthr*niter
					old_result_dir = "$(old_dis_dir)/r$(i)"
					new_result_dir = "$(new_dis_dir)/r$(i)"
					(!isdir(new_result_dir)) && (mkdir(new_result_dir))

					oldf = open("$(old_result_dir)/disorder", "r")
					disorder_str = readlines(oldf)
					close(oldf)

					newf = open("$(new_result_dir)/disorder", "w")
					disorder_float = parse.(Float64, disorder_str)
					disorder_float[1:l] .*= (w / W)
					for d in disorder_float
						println(newf, d)
					end
					close(newf)

					cmd = `$(peng_dir) $(length(disorder_float)) $disorder_float $(new_result_dir)`
					run(cmd)
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
