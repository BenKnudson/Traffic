#traffic main file
#Ben, Richard, Michael, Kelly
#
print 'Loading...'

import random
import numpy
import pylab as py
import Tkinter as tk

#begin function definitions
def traffic2(n,l,time,mv,lane): 			# Now with lanes!
	'''
	n = number of cars
	l = length of road (l > n)
	time = number of time steps to be taken
	mv = Max velocity
	lane = number of lanes  '''
	
	loc = numpy.zeros((lane,time+1,n), dtype=numpy.int) #location
	vel = numpy.zeros((lane,time+1,n), dtype=numpy.int) #velocity
	dis = numpy.zeros((lane,time+1,n), dtype=numpy.int) #distance to car ahead in same lane
	agg = numpy.zeros((lane,time+1,n), dtype=numpy.int) #aggrevation value
	pv0 =  numpy.random.rand(n)
	pv = [int(mv*(0.90+0.20*a)) for a in pv0] #make a preferred velocity 
	bold0 = numpy.random.rand(n)
	bold = [numpy.floor(10*a)+1 for a in bold0] #make boldness
	
	posloc0 = range(l*lane)
	posloc = [a+1 for a in posloc0]
	
	
	for i in range(n): #set initial velocities and lane values
		choice = random.choice(posloc)
		posloc.remove(choice)
		lc = choice/l#choose random lane
		vel[lc-1,0,i] = random.randint(0, mv)
		loc[lc-1,0,i] = choice%l #set initial locationsposloc.remove(loc[lc-1,0,i])#avoid cars starting on top of each other (we don't want pile-ups)
	tr1 = range(time)
	tr = [a+1 for a in tr1]
	
	for t in tr:
		for h in range(lane):
			for k in range(n):# find distances
				same = [loc[h,t-1,k]]*n
				dif = numpy.array([a-b for a,b in zip(same,loc[h,t-1,:])])
				dis_standin = numpy.where(dif<0)
				if len(dif[dis_standin]) > 0:
					dis[h,t-1,k] = min(abs(-1*dif[dis_standin]))
				else:
					dis[h,t-1,k] = l-max(dif)
					
				if vel[h,t-1,k] < pv[k]:   #Changing velocities for next step#approach preferred velocity
					vel[h,t,k] = vel[h,t-1,k]+((bold[k]+agg[h,t-1,k])/10)*(pv[k] - vel[h,t-1,k]) #speed up
					if agset==1:
						agg[h,t,k]= agg[h,t-1,k]+1
				elif vel[h,t-1,k] > pv[k]:
					vel[h,t,k] = vel[h,t-1,k]-((bold[k]+agg[h,t-1,k])/10)*(pv[k] - vel[h,t-1,k]) #slow down
				else:
					vel[h,t,k] = vel[h,t-1,k]
				
				if dis[h,t,k] == 1: #use environment to change velocity
					vel[h,t,k] = 0
					if agset==1:
						agg[h,t,k]= agg[h,t-1,k]+3
				elif dis[h,t,k] <= vel[h,t-1,k]: 
					if agset==1:
						agg[h,t,k]= agg[h,t-1,k]+2
					if dis[h,t,k] <= numpy.floor((1/2)*vel[h,t-1,k]):
						vel[h,t,k] = dis[h,t-1,k]-1
					else:
						vel[h,t,k] = vel[h,t-1,k]-1       ######
				elif dis[h,t,k] > vel[h,t,k]+int(vel[h,t,k]/(bold[k]+agg[h,t-1,k])): ######
					vel[h,t,k] = vel[h,t,k]+1  ######
				else:
					vel[h,t,k] = vel[h,t-1,k]        #####t-1 flag
				
				if agg[h,t,k]==0 and agg[h,t-1,k]>0:
					agg[h,t,k]=agg[h,t-1,k]-1
				
				ranbreakprob = 10*numpy.random.rand(1)
				if ranbreakprob < 1 and vel[h,t,k]>0:
					vel[h,t,k] = vel[h,t,k]-int(0.2*vel[h,t,k])   ####ben changed the percent of braking
					
				loc[h,t,:] = loc[h,t-1,:]+vel[h,t,:]
				
			for s in range(n):
				if loc[h,t,s] >= l:
					loc[h,t,s] = loc[h,t,s]-l
					
	passdic = dict()
	passdic['distance'] = dis
	passdic['location']=loc
	passdic['velocity']=vel
	return passdic   
   

def simulation(l,time,mv,lane):
	'''
	args (length, time, maxvelocity, lane)
	calls traffic2(#cars,length, time, maxvelocity,lane)
	Michael Lee
	'''
	#initialize variables
	velarray = numpy.zeros((time))
	avgvelocity = numpy.zeros((l))
	avgcurrent = numpy.zeros((l))
	velocity = dict()
	loc = dict()
	
	for i in range(l): #runs the traffic simulation from from 1 car per lane to a car density of 1
		passdic = traffic2(i+1,l,time,mv,lane)
		velocities = passdic['velocity']
		velocity[i] = passdic['velocity']
		loc[i] = passdic['location']
		
		for k in range(time): #builds an array of the total velocity at each point in time
			velarray[k] = sum(sum(velocities[:,k,:]))
		
		avgvelocity[i] = sum(velarray)/((i+1)*lane) #builds an array of the average velocity for each density
		avgcurrent[i] = avgvelocity[i]*(i+1)/l  #builds an array of the average current for each density  
	d = py.arange(1./l,1+1./l,1./l)
	py.plot(d,avgcurrent)
	py.ylim(0,(max(avgcurrent)+1))
	py.xlabel('density')
	py.ylabel('average current')
	py.title('Traffic Current')
	py.grid(True)
	py.show()
	return velocity,loc


def runONE(l,time,mv,lane):
	'''
	This is a subrun of simulation. it only runs one density.
	'''
	#initialize variables
	velarray = numpy.zeros((time))
	avgvelocity = numpy.zeros((l))
	avgcurrent = numpy.zeros((l))
	velocity = dict()
	loc = dict()
	n = int(density*l*lane) 
	passdic = traffic2(n,l,time,mv,lane)
	velocities = passdic['velocity']
	velocity[1] = passdic['velocity']
	loc[1] = passdic['location']
	
	for k in range(time): #builds an array of the total velocity at each point in time
		velarray[k] = sum(sum(velocities[:,k,:]))
		
	d = py.arange(1./l,1+1./l,1./l)
	return velocity,loc


def Space_Time_Plot(l,time,lane,density,trafficinfo): 
    '''
	Need to run simulation function to get trafficinfo variable
	Density needs to match one of the possible densities from the number of spaces exactly, i.e. if there are 10 spaces then only densities that are multiples of 0.1 are valid.

	l, time, and lane all must match the variables used in Simulation
	returns information necessary to run the Traffic_Animation function

	this function currently only operates when a single lane is used
	'''
    import pylab as py
    spacefunctions = dict()
    spaceplots = dict()
    
    n = int(density*l*lane) #determines the car number that the user wants to plot
    
    initpositions = trafficinfo[1][n-1][:,0,:][0]
    
    
    #gets the cars' initial positions
    for i in range(n):
        spacefunctions[i]=[initpositions[i]]
        
    # builds a dictionary of lists with all the cars' distance traveled over the length of the simulation
    for i in range(time-1):
        for j in range(n):
            spacefunctions[j].append(trafficinfo[0][n-1][0,i+1,j]+spacefunctions[j][i])
    
    # builds a dictionary of each car's individual space time plot before showing all of them together
    t = py.arange(0,time,1)
    for i in range(n):
        spaceplots[i] = py.plot(spacefunctions[i],t)
    
    py.xlabel('Space')
    py.ylabel('Time')
    py.title('Traffic Simulation Space/Time Plot for Density %s'%(density))
    py.show()
    
    return spacefunctions

def Space_Time_PlotONE(l,time,lane,density,trafficinfo):
    '''
	This is a version of STP that only uses one data set. faster
	'''
    spacefunctions = dict()
    spaceplots = dict()
    n = int(density*l*lane) #determines the car number that the user wants to plot
    initpositions = trafficinfo[1][1][:,0,:][0] #[loc (not vel)][time][relic]
    #gets the cars' initial positions
    for i in range(n):
        spacefunctions[i]=[initpositions[i]]
        
    # builds a dictionary of lists with all the cars' distance traveled over the length of the simulation
    for i in range(time-1):
        for j in range(n):
            spacefunctions[j].append(trafficinfo[0][1][0,i+1,j]+spacefunctions[j][i])
    
    # builds a dictionary of each car's individual space time plot before showing all of them together
    t = py.arange(0,time,1)
    for i in range(n):
        spaceplots[i] = py.plot(spacefunctions[i],t)
    
    py.xlabel('Space')
    py.ylabel('Time')
    py.title('Traffic Simulation Space/Time Plot for Density %s'%(density))
    py.show()
    
    return spacefunctions


def Traffic_Animation(space,l,time,lane,density,delay):
    '''
	
	Note that the Space Time plot function must be run before the Traffic
	Animation and that they must both use the same density

	'space' is the variable returned by the Space Time Plot Function
	l, time, and lane must match the variables used in Space_Time_Plot and
	simulation
	delay let's the user set how quickly the animation plays

	Early termination of the animation window will cause the function to return
	an error that will cause the the main program to crash

	Animation currently only works with a single lane
	'''
    import Tkinter as tk
    import numpy as np
    
    # initialize variables
    cars = dict()
    v = dict()
    spots = dict()
    n = int(density*l*lane)
    w = 1200/l #scales the size of the cars
    
    window = tk.Tk()
    canvas = tk.Canvas(window, width = 1200, height = lane*(w+50))
    canvas.pack()
    
    # creates the cars with a properly scales size
    for i in range(n):
        cars[i] = [canvas.create_rectangle(w*space[i][0],20,w*space[i][0]+w,20+w,fill="red")]
        cars[i].append(w*space[i][0])
    
    # creates lines to mark discrete road positions
    for i in range(l-1):
        spots[i] = canvas.create_line(w*(i+1),0,w*(i+1),lane*(w+50))
    
    # creates dictionary of velocities for all the cars
    for k in range(n):
        v[k] = []
    
    for t in range(time - 1):
        for k in range(n):
            p1 = space[k][t]
            p2 = space[k][t+1]
            v[k].append(int((round((p2 - p1)*w/10))))
    
    
    # plays the animation
    for t in range(time - 1):
        # breaks each car's movements into 10 movements to smooth out the visualization
        for p in range(10):
            for i in range(n):
                # if the car travels out of the window it resets it at the begining of the window
                if cars[i][1] < 1200:
                    dx = v[i][t]
                else:
                    dx = -(1200 - v[i][t])
                cars[i][1] += dx
                canvas.move(cars[i][0],dx,0)
                canvas.after(delay)
                canvas.update()

    window.mainloop()


#initialization
#default values 
l = 40
time = 40
mv = 15
lane = 1
density=0.6
agset=0
delay=4
trafficinfo=[-1,-1] #dummy traffic info for fail check

done=False
print 'Welcome to Traffic'
menu1= '''
Main Menu 
1- Options 
2- Run once
3- Position Graph of cars
4- Simulate multiple densities
5- Animation
q-[quit]'''
credits= '''
Ben, Richard, and Michael thank you for your interest in Traffic!
Traffic was programmed in Python
for PHYS 400, Cal Poly Physics Department
May 30, 2012
'''

print menu1
while done !=True:				# main program loop
	d=False
	c=raw_input('Enter Choice: ')
	if c == '1': 	##set options sub menu
		while d!=True:
			print '\nCurrent settings'
			print '1-Road length:     ' + str(l)
			print '2-Number of lanes: ' + str(lane)
			print '3-Car density:     ' + str(density)
			print '4-Max velocity     ' + str(mv)
			print '5-Time steps       ' + str(time)
			print '6-agrivation on/off [1,0] ' + str(agset)
			print '7-animation delay  ' + str(delay)
			print '0-[return]'
			e=0
			e=raw_input('Enter Choice to change: ')
			if e=='1':
				l=raw_input('Enter length of road: ')
				l=int(l)
			elif e=='2':
				lane=raw_input('Enter number of lanes: ')
				lane=int(lane)
			elif e=='3':
				density=raw_input('Enter car density: ')
				density=float(density)
			elif e=='4':
				mv=raw_input('Enter max velocity: ')
				mv=float(mv)
			elif e=='5':
				time=raw_input('Enter number of time steps: ')
				time=int(time)
			elif e=='6':
				agset=raw_input('Agrivation 1/0: ')
				agset=int(agset)
			elif e=='7':
				delay=raw_input('Enter Animation delay time: ')
				delay=int(delay)
			elif e=='0':
				print menu1
				d=True
			else :
				print menu1
				d=True
				
	elif c=='4':			##run world	
		print 'runing!...'					
		trafficinfo = simulation(l,time,mv,lane)
		space = Space_Time_Plot(l,time,lane,density,trafficinfo)  
		print 'Caluculations complete. Would you like to see car position graph? [y/n]'
		c2=raw_input('')
		if c2=='y':
			print 'opening Graphs...'
			space=Space_Time_Plot(l,time,lane,density,trafficinfo)
			
	elif c=='2':
		print 'runing once...'
		trafficinfo=runONE(l,time,mv,lane)
		
	elif c=='3': 				## see graphs of locations
		if trafficinfo[0]<0:
			print 'Error. Must run first.'
		else:
			print 'opening Graphs...'
			space= Space_Time_PlotONE(l,time,lane,density,trafficinfo)
		
	elif c=='5':                   ## animation of cars on road
		if trafficinfo[0]<0:
			print 'Error. Must run first.'
		else:		
			print 'Opening visualizer...'
			Traffic_Animation(space,l,time,lane,density,delay)
			
	elif c=='m':            #menu command
		print menu1
		
	elif c=='q': 			## quit
		done=True
		
	else:
		print 'Invalid Choice.'
		
print credits
print 'Done.'