from vpython import *
from gui_control import *
import atexit
import math

##########################
###### GLOBAL VARS  ######
##########################

class g: 
    radius_big = 50
    radius_roller = 10
    radius_tracker = 3
    
    

##########################
##### TIME CLASS #####
##########################

class time:
    t = 0
    end = 13000
    delta = 0.3
    rate = 500



##########################
######  AXIS CLASS  ######
##########################

class axis:
    def __init__(self, length):
        self.yaxis = arrow(pos=vector(0,-length,0), axis=vector(0, length << 1,0), shaftwidth=5, color=color.green, headwidth = 5 ) 
        self.xaxis = arrow(pos=vector(-length,0,0), axis=vector(length << 1,0,0), shaftwidth=5, color=color.red, headwidth = 5 )
        self.zaxis = arrow(pos=vector(0,0,-length), axis=vector(0,0,length << 1), shaftwidth=5, color=color.blue, headwidth = 5 )
    








##########################
######     MAIN     ######
##########################

if __name__ == "__main__":

    # create the scene
    scene = canvas(height=1500,width=1020)

    # plot coordinate grid
    grid = axis(200)

    # create simulation and add planets

    while time.t < time.end:
        # rate limit loop
        rate(100)
        # print(time.t)

        # monitor keyboard inputs
        monitor_loop()

        # update simulation
        # update code here

        # increment time
        time.t += time.delta

    while(True):
        monitor_loop()
        


