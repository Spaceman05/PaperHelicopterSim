import numpy as np
from matplotlib import pyplot as plt
import os

class GlobalAxes:
    ## Subplot for run comparisons
    fig = plt.figure(figsize = (16, 8))
    axVelocity = plt.subplot(4, 3, 1, ylabel = "Downward Velocity")
    axAngularV = plt.subplot(4, 3, 2, ylabel = "Angular Velocity")
    axAcceleration = plt.subplot(4, 3, 4, ylabel = "Downward Acceleration")
    axAngularA = plt.subplot(4, 3, 5, ylabel = "Angular Acceleration")
    axBladeAngle = plt.subplot(4, 3, 3, ylabel = "Blade Angle")



class SingleRun:
    def __init__(self, filename):
        
        with open(filename, "r") as dat:
            while (line := dat.read()) != "":
                exec(line)

        GlobalAxes.axVelocity.plot(self.tAxis, self.vzAxis)
        GlobalAxes.axAngularV.plot(self.tAxis, self.vthetaAxis)
        GlobalAxes.axAcceleration.plot(self.tAxis, self.azAxis)
        GlobalAxes.axAngularA.plot(self.tAxis, self.athetaAxis)
        GlobalAxes.axBladeAngle.plot(self.tAxis, self.bladeAngleAxis)

runs = [SingleRun("data\\" + file) for file in os.listdir("data")]

plt.show()
