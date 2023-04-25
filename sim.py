from vpython import *
from gui_control import *
import atexit
import math

##########################
###### GLOBAL VARS  ######
##########################

class g: 
    radius_big = 100
    radius_roller = 74
    rolling_speed = 100/radius_roller-1

    radius_tracker = 0.5
    ring_thickness = 0.5
    inner_ring_omega = -0.01
    tracker_omega = -inner_ring_omega
    
    

##########################
##### TIME CLASS #####
##########################

class time:
    t = 0
    end = 13000
    delta = 0.3
    rate = 200
    # rate = 5



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
        self.tail_tracker = sphere(radius = 1, pos=self.pos_tail, make_trail = True, color = color_in, visible = True)
        self.head_tracker = sphere(radius = 1, pos=self.pos_head, make_trail = True, color = color.purple, visible = False)
        self.place_pos(pos)

    # pos indicates where you want the end to placed, where the head** is placed
    def place_pos(self, pos_in : vector):
        vec_mag = self.length
        vec_norm = norm(self.rect.axis)
        self.rect.pos = pos_in
        self.rect.pos.x += vec_mag * vec_norm.x/2
        self.rect.pos.y += vec_mag * vec_norm.y/2

        # update head and tail of the rectangle
        self.pos_head = pos_in
        self.pos_tail = self.pos_head + self.rect.axis

        self.tail_tracker.pos = self.pos_tail
        self.head_tracker.pos = self.pos_head

    # update the direction in which the rectangle points
    def place_axis(self, axis_in : vector):
        # extend a vector's magnitude but maintain direction
        self.rect.axis = hat(axis_in) * mag(self.rect.axis)
        self.place_pos(self.pos_head)
    
    # rotate about self.head
    def rotate(self, angle_in, axis_in):
        self.rect.rotate(angle = angle_in, axis = axis_in, origin=self.pos_head)

        # update tail pos
        self.pos_tail = self.rect.axis + self.pos_head

        self.tail_tracker.pos = self.pos_tail
        self.head_tracker.pos = self.pos_head

    def reset_trail(self):
        self.tail_tracker.clear_trail()

    def visibility(self, isVisible):
        self.tail_tracker.visible = isVisible
        self.rect.visible = isVisible




class hypocycloid:
    def __init__(self, color_in):
        self.outerring = ring(pos = vector(0,0,0), axis = vector(0,0,1), radius = g.radius_big, thickness = g.ring_thickness, color = color_in)
        self.innerring = ring(pos = vector(0,g.radius_big-g.radius_roller,0), axis = vector(0,0,1), radius = g.radius_roller, thickness = g.ring_thickness, color = color_in)
        # self.tracker = sphere(pos=vector(0,g.radius_big,0), radius = g.radius_tracker, color=color.red, make_trail = True)

        self.arm = new_rect(pos=vector(0,g.radius_big-g.radius_roller,0), length_dim= g.radius_roller, side_dim=1, color_in=color.red)
        self.arm.place_axis(vector(0,1,0))
        self.arm.reset_trail()

    def update(self):
        self.innerring.rotate(angle=g.inner_ring_omega, axis=vector(0,0,1), origin=vector(0,0,0))
        # self.tracker.rotate(angle =g.inner_ring_omega, axis = vector(0,0,1), origin= vector(0,0,0))
        self.arm.place_pos(self.innerring.pos)
        self.arm.rotate(-g.inner_ring_omega*g.rolling_speed, axis_in=vector(0,0,1))

        # self.tracker.pos = self.arm.pos_tail
        # self.tracker.rotate(angle = -g.inner_ring_omega*2, axis = vector(0,0,1), origin = self.innerring.pos)

    def visibility(self, isVisible):
        self.outerring.visible = isVisible
        self.innerring.visible = isVisible
        self.arm.visibility(isVisible)

        



##########################
######     MAIN     ######
##########################

if __name__ == "__main__":

    # create the scene
    scene = canvas(height=800,width=800)

    # plot coordinate grid
    # grid = axis(200)

    # create simulation
    hpc = hypocycloid(color.orange)

    # declare variables
    visible = False
    run_once = False

    # tune the scene
    scene.autoscale = False

    while time.t < time.end:
        # rate limit loop
        rate(time.rate)
        # print(time.t)

        # monitor keyboard inputs
        monitor_loop()
        
        if(keyboard.is_pressed('shift+h') and run_once == False):
            visible = not visible
            hpc.visibility(visible)
            run_once = True
        elif(not keyboard.is_pressed('shift+h')):
            run_once = False


        # update simulation
        hpc.update()

        # increment time
        time.t += time.delta

    while(True):
        monitor_loop()
        


