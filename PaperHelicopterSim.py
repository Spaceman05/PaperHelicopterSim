## Written By Felix Black

## This code uses Python 3.9 and may contain the "Walrus" operator :=
## If you are not familiar, it assigns variables from within calculations

#import numpy as np
#from matplotlib import pyplot as plt
#import pygame

class Sim:
    ## This class is a container for global constants
    dt = 0.01
    Grav = 1

class Helicopter:
    ## This class manages variables of the test object
    def __init__(self, bladeLen, bladeWid, coreLen, coreWid, mass):
        self.bladeLen = bladeLen
        self.bladeWid = bladeWid
        self.coreLen = coreLen
        self.coreWid = codeWid
        self.mass = mass

                        ## Z-Coordinate is irrelevant since the environment is uniform
        self.theta = 0  ## Current angle of the object

        self.dz = 0     ## Downward motion
        self.dtheta = 0 ## Angular motion

        self.d2z = 0    ## Downward acceleration
        self.d2theta = 0 # Angular acceleration

    def simulate(self):


        self.dtheta += self.d2theta * Sim.dt    ## Change angular velocity by angular acceleration
        self.theta += self.dtheta * Sim.dt      ## Change angle by angular velocity

    def airDrag(self):
        
