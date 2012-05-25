from Tkinter import *
from random import *

window = Tk()
canvas = Canvas(window, width = 1200, height = 600)
canvas.pack()
n = 300
A = randint(0,10,n)
B = randint(0,10,n)
C = randint(0,10,n)
x0 = 10
y0 = 75
x1 = 60
y1 = 125
y2 = 275
y3 = 325
y4 = 475
y5 = 525
i = 0
Car1 = canvas.create_rectangle(x0,y0,x1,y1,fill="red", tag='redCar')
Car2 = canvas.create_rectangle(x0,y2,x1,y3,fill="blue", tag='bluCar')
Car3 = canvas.create_rectangle(x0,y4,x1,y5,fill="yellow", tag='yelCar')
lane1 = canvas.create_line(0,200,1200,200,tag='lane1')
lane2 = canvas.create_line(0,400,1200,400,tag='lane2')
j = 1
while j < n:
    deltax1 = A[j]
    deltax2 = B[j]
    deltax3 = C[j]
    canvas.move('redCar', deltax1, 0)
    canvas.move('bluCar', deltax2, 0)
    canvas.move('yelCar', deltax3, 0)
    canvas.after(20)
    canvas.update()
    j += 1
window.mainloop()
