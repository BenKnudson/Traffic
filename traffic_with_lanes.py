#Traffic.with.lanes
#richard

#n = number of cars
#l = length of road (l > n)
#time = number of time steps to be taken
#mv = Max velocity
#lane = number of lanes
 import random
 import numpy
 
def traffic2(n,l,time,mv,lane):# Now with lanes!
   
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
        lc = choice/l#choose random lane
        vel[lc-1,0,i] = random.randint(0, mv)
        loc[lc-1,0,i] = choice%l#set initial locations
        posloc.remove(choice)#avoid cars starting on top of each other (we don't want pile-ups)

    tr1 = range(time)
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
                
            #Changing velocities for next step
              #approach preferred velocity
                if vel[h,t-1,k] < pv[k]:
                    vel[h,t,k] = vel[h,t-1,k]+(bold[k]/10)*(pv[k] - vel[h,t-1,k]) #speed up
                elif vel[h,t-1,k] > pv[k]:
                    vel[h,t,k] = vel[h,t-1,k]-(bold[k]/10)*(pv[k] - vel[h,t-1,k]) #slow down
                else:
                    vel[h,t,k] = vel[h,t-1,k]
               #use environment to change velocity
                if dis[h,t,k] == 1:
                    vel[h,t,k] = 0
                elif dis[h,t,k] <= vel[h,t-1,k]: 
                    if dis[h,t,k] <= numpy.floor((1/2)*vel[h,t-1,k]): 
                        vel[h,t,k] = dis[h,t-1,k]-1
                    else:
                        vel[h,t,k] = vel[h,t-1,k]-1
                elif dis[h,t,k] > vel[h,t,k]+int(vel[h,t,k]/bold[k]):
                    vel[h,t,k] = vel[h,t,k]+1
                else:
                    vel[h,t,k] = vel[h,t,k]
                
                ranbreakprob = 10*numpy.random.rand(1)
                if ranbreakprob < 1 and vel[h,t,k]>0:
                    vel[h,t,k] = vel[h,t,k]-int(0.2*vel[h,t,k])


            loc[h,t,:] = loc[h,t-1,:]+vel[h,t,:]
            
            for s in range(n):
                if loc[h,t,s] >= l:
                    loc[h,t,s] = loc[h,t,s]-l
                    
                    
    passdic = dict()
    passdic['distance'] = dis
    passdic['location']=loc
    passdic['velocity']=vel
    return passdic
	
print traffic2(3,10,3,3,2)  #call
