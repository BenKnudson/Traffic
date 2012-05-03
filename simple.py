#simple traffic model
#bjknudson
import numpy as np


b=[]
for i in range(25):
    b.append(int(1.5*np.random.rand(1)))   #populate the lane b with cars 1 only those random numbers above 1 become cars
                   
for i in range(25):           #iterations of time
    print b
    for i in range(24):       #move through the lane and cars move if there is space to do so
        if b[24-i]==0:        #start with the end and work to the begining to update cars
            if b[23-i]==1:
                b[24-i]=1
                b[23-i]=0
    b[0]=int(1.5*np.random.rand(1))       #source of new cars entering at b[c]
            
print b    