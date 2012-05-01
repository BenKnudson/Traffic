Traffic
=
bjknudso

Prject Plan
======

program flow

1. Top level imput data
2. Background data production/manipulation based on (1)
3. Visualization/output



	Menu loop
		settings and options loop #Kelly
			a short interactive menu for inputing lane and car options
		end
	
		build #Richard/Ben
			This is where we do our stats to make the world of traffic (cars and lanes)
			Build given a car density parameter (assume given type float) and a number of lanes (assume given type int)
			spaces with cars are 1s and spaces without cars are 0s
			no speed or personality information is used
		end
    
		run #Richard/Ben
			iterate over time loop
				Takes a complete world in the form of a numpy array
				(type int with 1s and 0s or type bool with Trues and Falses) and 
				performs the updates with a specified updating function
			end
		end
	
	
		visualizer  #Michael
			takes array(s) of numpy with Trues and Falses type bool 
			or 1s and 0s type bool or int and translates them to graphs or colors 
		
		end

	end

