# Traffic world builder
# makes the world with cars and roads for traffic
# Richard, Ben, Michael, Kelly

import numpy as np

#build one car.
def buildcar(id):
	spd=int(65+10*np.random.rand(1)) #make prefered spd between 55 and 75 mean 65 mph
	rt=int((0.2+0.4*np.random.rand(1) )*100) #make reaction time between in seconds
	carnum=id*100000000+spd*1000000+rt*10000+spd #build car number that contains personality
	print carnum
	return carnum #carnum contatins [id]:[prefspd]:[reaction time]:[currentent acceleration]:[current spd]

#what is the car and what is it doing right now
def carinfo(carnum):
	print 'Carinfo'
	id=abs(carnum/100000000) #id number
	spd= abs(carnum%100)  #spd
	accel= carnum/100%100 #accel
	react=abs(carnum/10000)%100/100.0 #rt
	prefspd=abs(carnum/1000000)%100 #pref spd
	return np.array([id,prefspd,react,accel, spd, int])


print carinfo(buildcar(1))
