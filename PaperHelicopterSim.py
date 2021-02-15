## Written By Felix Black

## This code uses Python 3.9 and may contain the "Walrus" operator :=
## If you are not familiar, it assigns variables from within calculations

import numpy as np
from matplotlib import pyplot as plt
#import pygame

class Sim:
    ## This class is a container for global values
    dt = 0.01
    Grav = 1    ## Gravitational acceleration
    AirDensity = 1

    t = 0

class Helicopter:
    ## This class manages variables of the test object
    def __init__(self, bladeLen, bladeWid, thickness, coreLen, coreWid, mass):
        self.bladeLen = bladeLen
        self.bladeWid = bladeWid
        self.thickness = thickness #thickness

        self.bladeArea = bladeLen * bladeWid
        self.bladeAngle = np.pi/4   ## The angle from vertical
        
        self.coreLen = coreLen
        self.coreWid = coreWid
        self.mass = mass

        ## Iblade = T * (L^2 + W^2) * (m/3)
        self.bladeMomentOfInertia = thickness * (bladeLen**2 + bladeWid**2)*mass/3

        ## Icore = T * L * W^2 * m/12
        self.coreMomentOfInertia = thickness * coreLen * (coreWid**2) * mass/12

        self.Itotal = self.coreMomentOfInertia + (2 * self.bladeMomentOfInertia)

                        ## Z-Coordinate is irrelevant since the environment is uniform
        self.theta = 0  ## Current angle of the object

        self.dz = 0     ## Downward motion
        self.dtheta = 0 ## Angular motion

        self.d2z = 0    ## Downward acceleration
        self.d2theta = 0## Angular acceleration


        ## Subplot for this object
        self.fig = plt.figure(figsize = (15, 5))
        self.axVelocity = plt.subplot(2, 2, 1, ylabel = "Downward Velocity")
        self.axAngularV = plt.subplot(2, 2, 2, ylabel = "Angular Velocity")
        self.axAcceleration = plt.subplot(2, 2, 3, ylabel = "Downward Acceleration")
        self.axAngularA = plt.subplot(2, 2, 4, ylabel = "Angular Acceleration")

    def simulate(self):
        self.d2z = 0
        self.d2theta = 0

        self.gravitate()
        self.airDrag()

        self.testRotate()

        self.dz += self.d2z * Sim.dt

        self.dtheta += self.d2theta * Sim.dt    ## Change angular velocity by angular acceleration
        self.theta += self.dtheta * Sim.dt      ## Change angle by angular velocity


        ## Plot the data from this iteration
        self.axVelocity.plot(Sim.t, self.dz, "b.")
        self.axAngularV.plot(Sim.t, self.dtheta, "b.")
        self.axAcceleration.plot(Sim.t, self.d2z, "b.")
        self.axAngularA.plot(Sim.t, self.d2theta, "b.")

        

    def gravitate(self):
        ## Cause the object to accelerate downwards
        self.d2z += self.mass * Sim.Grav

    def airDrag(self):
        ## Cause the object to decelerate due to air resistance
        # upward F = 1/2 rho v^2 Cd A
        # then x2 for 2 blades

        self.d2z -= Sim.AirDensity * (self.dz)**2 * self.bladeArea/ self.mass

        ## Cause the object to angularly decelerate due to the same (windward side of the edge of the paper)
        # backward torque, tau = 1/8 rho omega^2 H [x^4](from a to b)

        ## Torque on the core
        self.d2theta -= self.Itotal * Sim.AirDensity * self.dtheta**2 * self.coreLen * (self.coreWid**4) / 32

        ## Torque on the blades
        self.d2theta -= self.Itotal * Sim.AirDensity * self.dtheta**2 * self.bladeWid * (self.bladeLen**2) / 4
        
    def testRotate(self):
        ## Apply a torque to the blades based on air resistance
        # tau = air drag * half blade width

        tau = self.bladeWid * (Sim.AirDensity * (self.dz)**2 * self.bladeArea/ self.mass)

        self.d2theta += tau / self.Itotal

def simLoop(objects):
    stop = False
    while not stop:
        for obj in objects:
            obj.simulate()

            Sim.t += Sim.dt
            plt.pause(Sim.dt)

helicopters = [Helicopter(1, 1, 0.1, 1, 1, 1)]
simLoop(helicopters)
