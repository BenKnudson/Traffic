#traffic main file
#Ben, Richard, Michael, Kelly
#
import random
import numpy
import pylab as py

def traffic2(n,l,time,mv,lane):# Now with lanes!
    
    road = numpy.zeros((lane,time+1,l+1), dtype=numpy.int) #the traffic world
    loc = numpy.zeros((lane,time+1,n), dtype=numpy.int) #location
    vel = numpy.zeros((lane,time+1,n), dtype=numpy.int) #velocity
    dis = numpy.zeros((lane,time+1,n), dtype=numpy.int) #distance to car ahead in same lane
    agg = numpy.zeros((lane,time+1,n), dtype=numpy.int) #aggrevation value

    posloc = range(l)
    for i in range(n): #set initial velocities and lane values
        lc = random.randint(0,lane-1)#choose random lane
        vel[lc,0,i] = random.randint(0, mv)
        loc[lc,0,i] = random.choice(posloc)#set initial locations
        posloc.remove(loc[lc,0,i])#avoid cars starting on top of each other (we don't want pile-ups)

    tr1 = range(time-1)
    tr = [a+1 for a in tr1]
    
    for t in tr:
        for h in range(lane):
            for k in range(n):
            # find distances
                same = [loc[h,t-1,k]]*n
                dif = numpy.array([a-b for a,b in zip(same,loc[h,t-1,:])])
                dis_standin = numpy.where(dif<0)
                if len(dif[dis_standin]) > 0:
                    dis[h,t-1,k] = min(abs(-1*dif[dis_standin]))
                else:
                    dis[h,t-1,k] = l-max(dif)
                #print t,k,loc[h,t-1,k],loc[h,t-1,:],dif,dis[h,t-1,k]
                    
            #Changing velocities for next step
                if dis[h,t-1,k] == 1:
                    vel[h,t,k] = 0
                elif dis[h,t-1,k] <= vel[h,t-1,k]:
                    if dis[h,t-1,k] <= numpy.floor((1/2)*vel[h,t-1,k]):
                        vel[h,t,k] = dis[h,t-1,k]-1
                    else:
                        vel[h,t,k] = numpy.floor(dis[h,t-1,k]/2)
                elif dis[h,t-1,k] > 2*vel[h,t-1,k]:
                    vel[h,t,k] = vel[h,t-1,k]+1
                else:
                    vel[h,t,k] = vel[h,t-1,k]
                if vel[h,t,k] >= mv:
                    vel[h,t,k] = mv

            loc[h,t,:] = loc[h,t-1,:]+vel[h,t,:]
            
            for s in range(n):
                if loc[h,t,s] >= l:
                    loc[h,t,s] = loc[h,t,s]-l
                    
            road[h,t,loc[h,t,:]] = 1
                    
                    
    passdic = dict()
    passdic['distance'] = dis
    passdic['road'] = road
    passdic['location']=loc
    passdic['velocity']=vel
    return passdic
def simulation(l,time,mv,lane):
    
    #initialize variables
    velarray = numpy.zeros((time))
    avgvelocity = numpy.zeros((l))
    avgcurrent = numpy.zeros((l))
    road = dict()
    distance = dict()
    

    for i in range(l): #runs the traffic simulation from from 1 car per lane to a car density of 1
        passdic = traffic2(i+1,l,time,mv,lane)
        velocities = passdic['velocity']
        distance[i] = passdic['distance']
        road[i] = passdic['road']
        
        for k in range(time): #builds an array of the total velocity at each point in time
            velarray[k] = sum(sum(velocities[:,k,:]))
        
        #builds an array of the average velocity for each density
        avgvelocity[i] = sum(velarray)/((i+1)*lane)
        #builds an array of the average current for each density
        avgcurrent[i] = avgvelocity[i]*(i+1)/l
    
    
        
    d = py.arange(1./l,1+1./l,1./l)
    py.plot(d,avgcurrent)
    
    py.ylim(0,(max(avgcurrent)+1))
    
    py.xlabel('density')
    py.ylabel('average current')
    py.title('Traffic Current')
    py.grid(True)
    py.show()
    
    return distance,road
def Space_Time_Plot(l,time,lane,density,trafficinfo):
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

	
#l = 10
#time = 10
#mv = 3
#lane = 1
#density=.5
#trafficinfo = simulation(l,time,mv,lane)



done=False
print 'Welcome to Traffic'
menu1= '''
Main Menu 
1- set options 
2- create world 
3- run 
q- quit'''

while done !=True:				# outer loop
	print menu1
	c=raw_input('Enter Choice: ')
	if c == '1': 			##set options sub menu
		print 'Options'
		l=raw_input('Enter length of road: ')
		l=int(l)
		lane=raw_input('Enter number of lanes: ')
		lane=int(lane)
		density=raw_input('Enter car density: ')
		density=float(density)
		mv=raw_input('Enter max velocity: ')
		mv=float(mv)
		time=raw_input('Enter number of time steps: ')
		time=int(time)
	elif c =='2':   		##Build world based on options
		print 'Build'
		
	elif c=='3':			##run world	
		print 'run!'					##visualize world
		trafficinfo = simulation(l,time,mv,lane)
		Space_Time_Plot(l,time,lane,density,trafficinfo)
	elif c=='q': 			## quit
		done=True
		
	else:
		print 'Invalid Choice.'
		
	
print 'Done.'