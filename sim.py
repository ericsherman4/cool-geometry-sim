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
    ring_thickness = 0.5
    inner_ring_omega = -0.05
    tracker_omega = -inner_ring_omega
    
    

##########################
##### TIME CLASS #####
##########################

class time:
    t = 0
    end = 13000
    delta = 0.3
    rate = 30



##########################
######  AXIS CLASS  ######
##########################

class axis:
    def __init__(self, length):
        self.yaxis = arrow(pos=vector(0,-length,0), axis=vector(0, length << 1,0), shaftwidth=5, color=color.green, headwidth = 5 ) 
        self.xaxis = arrow(pos=vector(-length,0,0), axis=vector(length << 1,0,0), shaftwidth=5, color=color.red, headwidth = 5 )
        self.zaxis = arrow(pos=vector(0,0,-length), axis=vector(0,0,length << 1), shaftwidth=5, color=color.blue, headwidth = 5 )


##################################
##### WRAPPER CLASS FOR REC ######
##################################

# wrapper class for box that places pos at the end of the rectangle rather than the center
# and also tracks the head and tail of the rectangle
# docs: https://www.glowscript.org/docs/VPythonDocs/box.html
class new_rect:
    # pos is where to place the end of the rectangle
    def __init__(self, pos : vector, length_dim, side_dim, color_in : color):
        self.rect = box(length = length_dim, width = side_dim, height= side_dim, color= color_in)
        self.pos_head = vector(0,0,0)
        self.pos_tail = vector(length_dim,0,0)
        self.length = length_dim
        self.place_pos(pos)

    # pos indicates where you want the end to placed
    def place_pos(self, pos_in : vector):
        vec_mag = self.length
        vec_norm = norm(self.rect.axis)
        self.rect.pos = pos_in
        self.rect.pos.x += vec_mag * vec_norm.x/2
        self.rect.pos.y += vec_mag * vec_norm.y/2

        # update head and tail of the rectangle
        self.pos_head = pos_in
        self.pos_tail = self.pos_head + self.rect.axis

    # update the direction in which the rectangle points
    def place_axis(self, axis_in : vector):
        # original approach, find angle between vectors and then rotate og vector
        # problem: need to determine sign for theta based on planets positions
        # theta = math.acos(dot(self.rect.axis, axis_in)/ mag(self.rect.axis) / mag(axis_in))
        # self.rect.rotate(angle = theta, origin = self.pos_head, axis = vector(0,0,1))

        # second approach
        # extend a vector's magnitude but maintain direction
        self.rect.axis = hat(axis_in) * mag(self.rect.axis)
        self.place_pos(self.pos_head)


class hypocycloid:
    def __init__(self):
        self.outerring = ring(pos = vector(0,0,0), axis = vector(0,0,1), radius = g.radius_big, thickness = g.ring_thickness)
        self.innerring = ring(pos = vector(0,g.radius_big-g.radius_roller,0), axis = vector(0,0,1), radius = g.radius_roller, thickness = g.ring_thickness)
        self.tracker = sphere(pos=vector(0,g.radius_big,0), radius = g.radius_tracker, color=color.red, make_trail = True)


    def update(self):
        self.innerring.rotate(angle=g.inner_ring_omega, axis=vector(0,0,1), origin=vector(0,0,0))
        self.tracker.rotate(angle=g.inner_ring_omega, axis = vector(0,0,1), origin= self.innerring.pos)
        self.tracker.rotate(angle=g.tracker_omega, axis = vector(0,0,1), origin= vector(0,0,0))



##########################
######     MAIN     ######
##########################

if __name__ == "__main__":

    # create the scene
    scene = canvas(height=1500,width=1020)


    # plot coordinate grid
    # grid = axis(200)q

    # create simulation
    hpc = hypocycloid()

    while time.t < time.end:
        # rate limit loop
        rate(time.rate)
        # print(time.t)

        # monitor keyboard inputs
        monitor_loop()

        # update simulation
        hpc.update()

        # increment time
        time.t += time.delta

    while(True):
        monitor_loop()
        


