Traffic
=======
A group project with the goal of modeling traffic flow
==
Ben, Richard, and Michael

Run Traffic from the terminal by calling 
	Python main.py
This will initialize all variables and function definitions.
To run default conditions, select (2)-Run, then (3)Graphs to see what you've calculated. 
Then (5) Animation to visualize the traffic you have simulated. 

To run a simulation of a all densities at given road length, lanes, and time steps,
run (4) Simulation from the main menu. This will output a current vs density plot. 
After you have run (4), the data for all densities is held in memory. 
To visualize the position vs time graph or the animation for any of these densities, 
simply select (3) Graph or (5) Animate.
To specify the density you wish to see, Select (1)Options > (3) density > <input 0 to 1>.
Return to the main menu and select (3) Graphs or (5) Animate. 

To change
road length
lanes
density
max velocity
time steps
aggrivation on/off
animation delay

choose (1) Options from the main menu.

Car attributes: 
=
Cars are randomly assigned prefered velocities based on a spread of +20 to -20 percent of max velocity. 
Cars are randomly assigned boldness values between 1 and 10 which 
determines how quickly a car will change their velocity giving changing conditions.

Random Breaking
=
a mechanism for random breaking is also included. At any one timestep, 
there is a 1 in 10 chance that a car will press the breaks and lose 20% of their current velocity.

Aggrivation option: default <off>
Aggrivation, if turned on, exasperates the effect of boldness on driving decisions. 
A car gains agrivation for every timestep they are not going their perferred velocity and 
twice as quickly if they are stopped. Aggrivation lessens if a car is allowed to go their perfered velocity. 
A high aggrivation level causes larger changes in car velocity. Cars are expected to use more of the allowed road. 


Behind the scenes
===
Traffic can be broken down into 4 functions.
===

Traffic2() creates the world and holds all the logic behind driving decisions. 
Simulation() runs Traffic2 for every possible car density given 
	the physical parameters of road length,lanes, and time steps.
	Simulation() returns the plot of traffic current vs density and position vs time of all cars.
Space_Time_Plot() Returns only the position vs time plot of all cars for the currently selected density 0 to 1.
Traffic_Animation() is the animated visualizer of traffic given the currently selected density 0 to 1.

Since 4-Simulation is a very very time consuming step, we have included shortcuts.
There are other functions that serve the user faster ways of 
getting specific data sets without having to run the entire simulation. 
In the main menu:
2-Run runs only the simulation for the currently selected density