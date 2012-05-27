#michaels animation simulation
#

def traffic2(n,l,time,mv,lane):# Now with lanes!
    import random
    import numpy
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
    import numpy
    import pylab as py
    
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
    
    return velocity,loc

    


def Space_Time_Plot(l,time,lane,density,trafficinfo):
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
    
def Traffic_Animation(space,l,time,lane,density):
    import Tkinter as tk
    import numpy as np
    
    cars = dict()
    
    n = int(density*l*lane)
    w = 1200/l
    window = Tk()
    canvas = Canvas(window, width = 1200, height = lane*(w+50))
    canvas.pack()
    
    for i in range(n):
        cars[i] = canvas.create_rectangle(w*space[i][0],20,w*space[i][0]+w,20+w,fill="red", tag=i)
        
    for k in range(time):
        for t in range(w):
            for i in range(n):
                canvas.move(i,space[i][k],0)
                canvas.after(20)
                canvas.update()

    
    window.mainloop()
    
Traffic_Animation(space,l,time,lane,0.5)


l = 10
time = 10
mv = 15
lane = 1

trafficinfo = simulation(l,time,mv,lane)
space = Space_Time_Plot(l,time,lane,0.5,trafficinfo)    
Traffic_Animation(space,l,time,lane,0.5)