## Written By Felix Black

## This code uses Python 3.9 and may contain the "Walrus" operator :=
## If you are not familiar, it assigns variables from within calculations

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Button as btn
from datetime import datetime

class Sim:
    ## This class is a container for global values
    dt = 0.01
    Grav = 9.8    ## Gravitational acceleration
    AirDensity = 1.22 * 1.28    ## Absorb the drag coefficient in here

    t = 0
    stop = False

class Helicopter:
    ## This class manages variables of the test object
    def __init__(self, bladeLen, bladeWid, thickness, coreLen, coreWid, mass):
        self.bladeLen = bladeLen
        self.bladeWid = bladeWid
        self.thickness = thickness #thickness

        self.bladeArea = bladeLen * bladeWid

        self.bladeRigidity = 2      ## The resistance to bending
        self.bladeAngle = np.pi/6   ## The angle from horizontal
        
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
        self.fig = plt.figure(figsize = (16, 5))
        self.axVelocity = plt.subplot(2, 3, 1, ylabel = "Downward Velocity")
        self.axAngularV = plt.subplot(2, 3, 2, ylabel = "Angular Velocity")
        self.axAcceleration = plt.subplot(2, 3, 4, ylabel = "Downward Acceleration")
        self.axAngularA = plt.subplot(2, 3, 5, ylabel = "Angular Acceleration")
        self.axBladeAngle = plt.subplot(2, 3, 3, ylabel = "Blade Angle")

        axExportBtn = plt.subplot(2, 3, 6)
        self.btnExport = btn(axExportBtn, "Export", hovercolor='0.95')
        self.btnExport.on_clicked(self.exportData)

    def simulate(self):
        self.d2z = 0
        self.d2theta = 0

        self.gravitate()
        self.airDrag()

        self.dragRotate()

        self.dz += self.d2z * Sim.dt

        self.dtheta += self.d2theta * Sim.dt    ## Change angular velocity by angular acceleration
        self.theta += self.dtheta * Sim.dt      ## Change angle by angular velocity


        ## Plot the data from this iteration
        self.axVelocity.plot(Sim.t, self.dz, "b.")
        self.axAngularV.plot(Sim.t, self.dtheta, "b.")
        self.axAcceleration.plot(Sim.t, self.d2z, "b.")
        self.axAngularA.plot(Sim.t, self.d2theta, "b.")
        self.axBladeAngle.plot(Sim.t, self.bladeAngle, "b.")

        ## If the system is stable, output and finish
        if self.d2z < 1e-6 and self.d2theta < 1e-3:
            self.exportData("")

    def gravitate(self):
        ## Cause the object to accelerate downwards
        self.d2z += Sim.Grav

    def airDrag(self):
        ## Cause the object to decelerate due to air resistance
        # upward F = 1/2 rho v^2 Cd A
        # then x2 for 2 blades

        self.d2z -= Sim.AirDensity * (self.dz**2) * self.bladeArea * (np.cos(self.bladeAngle)**2) / self.mass

        ## Cause the object to angularly decelerate due to the same (windward side of the edge of the paper)
        # backward torque, tau = 1/8 rho omega^2 H [x^4](from a to b)

        ## Torque on the core
        self.d2theta -= Sim.AirDensity * (self.dtheta**2) * self.coreLen * (self.coreWid**4) / (self.Itotal * 32)
        

    def dragRotate(self):
        ## Apply a torque to the blades based on air resistance
        # tau = air drag * half blade width

        F = Sim.AirDensity * (self.dz**2) * self.bladeArea * np.cos(self.bladeAngle)

        tau = F * np.sin(self.bladeAngle) * self.bladeWid / 2

        self.d2theta += tau / self.Itotal



    def exportData(self, event):
        ## Write the data to a .txt file, can be loaded back in using exec()
        with open("data\/" + datetime.now().strftime("%m_%d_%y__%H_%M_%S_%f") + ".txt", "w") as dat:
            dat.write("self.bladeLen = "   + str(self.bladeLen))
            dat.write("\nself.bladeWid = " + str(self.bladeWid))
            dat.write("\nself.thickness = "+ str(self.thickness))
            dat.write("\nself.bladeArea = "+ str(self.bladeArea))
            dat.write("\nself.bladeRigidity = " + str(self.bladeRigidity))
            dat.write("\nself.coreLen = "  + str(self.coreLen))
            dat.write("\nself.coreWid = "  + str(self.coreWid))
            dat.write("\nself.mass = " + str(self.mass))
            dat.write("\n")
            dat.write("\nself.tAxis = " + str([round(Line.get_xdata()[0], 15) for Line in self.axVelocity.lines]))
            dat.write("\nself.vzAxis = " + str([round(Line.get_ydata()[0], 15) for Line in self.axVelocity.lines]))
            dat.write("\nself.vthetaAxis = " + str([round(Line.get_ydata()[0], 15) for Line in self.axAngularV.lines]))
            dat.write("\nself.azAxis = " + str([round(Line.get_ydata()[0], 15) for Line in self.axAcceleration.lines]))
            dat.write("\nself.athetaAxis = " + str([round(Line.get_ydata()[0], 15) for Line in self.axAngularA.lines]))
            dat.write("\nself.bladeAngleAxis = " + str([round(Line.get_ydata()[0], 15) for Line in self.axBladeAngle.lines]))

        Sim.stop = True
        plt.close()
            

def simLoop(helicopterObject, headless):
    ## Reset
    Sim.stop = False
    Sim.t = 0
    
    while not Sim.stop:
        helicopterObject.simulate()

        Sim.t += Sim.dt
        if not headless:    ## Only dislay graphs if headless is False
            plt.pause(Sim.dt)

for w, width in enumerate(np.arange(0.05, 0.165, 0.005)):
    for l, length in enumerate(np.arange(0.08, 0.205, 0.005)):
        print(str(w) + ", " + str(l) + ":\t" + str(round(width, 3)) + ", " + str(round(length, 3)))
        simLoop(Helicopter(round(length, 3), round(width, 3), 0.001, 0.05, 0.05, 0.005), True)
    
