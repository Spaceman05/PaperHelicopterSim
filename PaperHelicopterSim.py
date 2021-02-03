## Written By Felix Black

## This code uses Python 3.9 and may contain the "Walrus" operator :=
## If you are not familiar, it assigns variables from within calculations

import numpy as np
#from matplotlib import pyplot as plt
#import pygame

class Sim:
    ## This class is a container for global constants
    dt = 0.01
    Grav = 1    ## Gravitational acceleration
    AirDensity = 1

class Helicopter:
    ## This class manages variables of the test object
    def __init__(self, bladeLen, bladeWid, bladeThk, coreLen, coreWid, mass):
        self.bladeLen = bladeLen
        self.bladeWid = bladeWid
        self.bladeThk = bladeThk #thickness

        self.bladeArea = bladeLen * bladeWid
        self.bladeAngle = np.pi/2
        
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
        self.d2z = 0
        self.d2theta = 0


        self.dtheta += self.d2theta * Sim.dt    ## Change angular velocity by angular acceleration
        self.theta += self.dtheta * Sim.dt      ## Change angle by angular velocity

    def gravitate(self):
        ## Cause the object to accelerate downwards
        self.d2z += self.mass * Sim.gravity

    def airDrag(self):
        ## Cause the object to deccelerate due to air resistance
        # upward F = 1/2 rho v^2 Cd A
        # then x2 for 2 blades

        d2z -= Sim.AirDensity * (self.dz)**2 * self.bladeArea/ m
