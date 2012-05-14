#Traffic.simple
#richard

#n = number of cars
#l = length of road (l > n)
#time = number of time steps to be taken
#mv = Max velocity
#lane = number of lanes

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
	
traffic2(3,10,3,3,2)  #call
