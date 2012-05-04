# Traffic world builder
# makes the world with cars and roads for traffic
# Richard, Ben, Michael, Kelly

import numpy as np

#build one car. takes car id number as a
def buildcar(id):
	'''builds one car number. 
	takes car id as argument.
	outputs car number with randomly generated characteristics for 
	prefered spd and reaction time, builds carnum with initial conditions of 
	accel=0 and spd=prefspd'''
	spd=int(65+10*np.random.rand(1)) #make prefered spd between 55 and 75 mean 65 mph
	rt=int((0.2+0.4*np.random.rand(1) )*100) #make reaction time between in seconds
	carnum=id*100000000+spd*1000000+rt*10000+spd #build car number that contains personality
	print carnum
	return carnum #carnum contatins [id]:[prefspd]:[reaction time]:[currentent acceleration]:[current spd]

#what is the car and what is it doing right now
def carinfo(carnum):
	'''takes car number as argument and translates it 
	into an np array of the car's characteristics 
	and current conditions for accel and spd'''
	print 'Carinfo'
	id=abs(carnum/100000000) #id number
	spd= abs(carnum%100)  #spd
	accel= carnum/100%100 #accel
	react=abs(carnum/10000)%100 #rt    note: raction time is still times ten so it's an int
	prefspd=abs(carnum/1000000)%100 #pref spd
	return np.array([id,prefspd,react,accel, spd, int])


print carinfo(buildcar(1))
