include("lurITensorTools.jl")

home_dir = "/home/gykim"
data_dir = "$(home_dir)/prx7/data"
peng_dir = "$(home_dir)/prx7/ed/peng_tisj_vs3"

function main()
	syssize = parse(Int64, ARGS[1])
	ls = [2, 4, 6, 0]
	w = 0.2
	Ws = [2, 3, 4, 5, 6, 8, 10, 12, 15]

	for l in ls	
		for W in Ws
			dis_dir = "$(data_dir)/p4_l$(l)_w$(w)_L$(syssize-l)_W$(W)"
			(!isdir(dis_dir)) && (mkdir(dis_dir))

			for rdir in readdir(dis_dir)
				result_dir = "$(dis_dir)/$(rdir)"
				(!isdir(result_dir)) && (mkdir(result_dir))

				try
					fname = "$(result_dir)/disorder"
					disorder = readlines(fname)
					if !isfile("$(result_dir)/tisj_a0_0")
						print("Checking $(result_dir)\t")
						cmd = `$(peng_dir) $(length(disorder)) $disorder $(result_dir)`
						run(cmd)
						println("success")
					end
				catch
					println("error")
				end
			end
		end
	end
end

if length(ARGS) != 1
	println("Usage : julia check_for_errs.jl <L>")
	exit(1)
end


main()
