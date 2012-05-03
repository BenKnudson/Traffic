#traffic main file
#Ben, Richard, Michael, Kelly
#

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
	
	elif c =='2':   		##Build world based on options
		print 'Build'
		
	elif c=='3':			##run world	
		print 'run!'					##visualize world
		
		
	elif c=='q': 			## quit
		done=True
		
	else:
		print 'Invalid Choice.'
		
	
print 'Done.'