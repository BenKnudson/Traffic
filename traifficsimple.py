#Traffic.simple 
#richard

#n = number of cars
#l = length of road
#time = number of time steps to be taken
#mv = Max velocity

def traffic1(n,l,time,mv):
    import random
    import numpy
    road = numpy.zeros((time+1,l+1), dtype=numpy.int)
    loc = numpy.zeros((time+1,n), dtype=numpy.int)
    vel = numpy.zeros((time+1,n), dtype=numpy.int)
    dis = numpy.zeros((time+1,n), dtype=numpy.int)

    loc[0,:] = random.sample(range(l), n)#set initial locations
    for i in range(n): #set initial velocities
        vel[0,i] = random.randint(0, mv)
    
    road[0,loc] = 1#vel #place initial velocities in initial conditions

    tr1 = range(time-1)
    tr = [a+1 for a in tr1]

    for t in tr:
    
        for k in range(n):
            same = [loc[t-1,k]]*n
            dif = numpy.array([a-b for a,b in zip(same,loc[t-1,:])])
            dis_standin = numpy.where(dif>0)
            if len(dif[dis_standin]) > 0:
                dis[t,k] = min(dif[dis_standin])
            else:
                dis[t,k] = sum([min(dif),l])
            if dis[t,k] <= vel[t-1,k]:
                vel[t,k] = numpy.floor(dis[t,k]/2)
            elif dis[t,k] > 2*vel[t-1,k]:
                vel[t,k] = vel[t-1,k]+1
            else:
                vel[t,k] = vel[t-1,k]
            if dis[t,k] >= mv:
                vel[t,k] = mv
            
        loc[t,:] = [sum(pair) for pair in zip(loc[t-1,:],vel[t,:])]
        for s in range(n):
            if loc[t,s] > 20:
                loc[t,s] = loc[t,s]-20
    
        road[t,loc[t,:]]= 1#vel[t,:]      
    
    passdic = dict()
    passdic['road'] = road
    passdic['location']=loc
    passdic['velocity']=vel
    return passdic
	
print traffic1(3,19,5,3)