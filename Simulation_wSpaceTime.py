#Need to run simulation function to get trafficinfo variable
#Density needs to match one of the possible densities from the number of spaces exactly, i.e. if there are 10 spaces then only densities that are multiples of 0.1 are valid.

def Space_Time_Plot(l,time,lane,density,trafficinfo):
    import pylab as py
    
    spacefunctions = dict()
    spaceplots = dict()
    
    n = int(density*l*lane) #determines the car number that the user wants to plot
    
    initpositions = trafficinfo[1][n-1][:,1,:][0]
    
    
    #gets the cars' initial positions
    k = 0
    for i in range(l):
        if initpositions[i] == 1:
            spacefunctions[k] = [i]
            k += 1
    
    
    # builds a dictionary of lists with all the cars' distance traveled over the length of the simulation
    for i in range(time-1):
        for j in range(n):
            spacefunctions[j].append(trafficinfo[0][n-1][0,i,j]+spacefunctions[j][i])
            
    
    
    # builds a dictionary of each car's individual space time plot before showing all of them together
    t = py.arange(0,time,1)
    for i in range(n):
        spaceplots[i] = py.plot(spacefunctions[i],t)
    
    py.xlabel('Space')
    py.ylabel('Time')
    py.title('Traffic Simulation Space/Time Plot for Density %s'%(density))
    py.show()
    
    
Space_Time_Plot(l,time,lane,0.5,trafficinfo)
