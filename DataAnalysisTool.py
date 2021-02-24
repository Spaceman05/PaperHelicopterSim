import numpy as np
from matplotlib import pyplot as plt
import os

class GlobalAxes:
    ## Subplot for run comparisons
    fig = plt.figure(figsize = (16, 9))
    axVelocity = plt.subplot(4, 2, 1, ylabel = "Downward Velocity ($m s^{-1}$)", xlabel = "time (s)", xlim = [0, 1.0])
    axAngularV = plt.subplot(4, 2, 2, ylabel = "Angular Velocity ($rad s^{-1}$)", xlabel = "time (s)", xlim = [0, 1.0])
    axAcceleration = plt.subplot(4, 2, 3, ylabel = "Downward Acceleration ($m s^{-2}$)", xlabel = "time (s)", xlim = [0, 1.0])
    axAngularA = plt.subplot(4, 2, 4, ylabel = "Angular Acceleration ($rad s^{-2}$)", xlabel = "time (s)" ,xlim = [0, 1.0], ylim=[-200, 4000])
    #axBladeAngle = plt.subplot(4, 3, 3, ylabel = "Blade Angle")

    axTerminalVWid = plt.subplot(4, 2, 5, xlabel = "Blade Width (m)", ylabel = "Terminal Velocity ($m s^{-1}$)")
    axTerminalVLen = plt.subplot(4, 2, 6, xlabel = "Blade Length (m)", ylabel = "Terminal Velocity ($m s^{-1}$)" , xlim = [0.07, 0.21])
    axTerminalThetaWid = plt.subplot(4, 2, 7, xlabel = "Blade Width (m)", ylabel = "Terminal Angular Velocity ($rad s^{-1}$)" , ylim = [0, 400])
    axTerminalThetaLen = plt.subplot(4, 2, 8, xlabel = "Blade Length (m)", ylabel = "Terminal Angular Velocity ($rad s^{-1}$)", xlim = [0.07, 0.21], ylim = [0, 400])

##    axColourKey = plt.axes([0.96, 0.25, 0.01, 0.5], xlabel = "Colour Key", ylabel = "Colour key: blade area ($m^2$)", ylim = [0, 0.035])
##    axColourKey.get_xaxis().set_visible(False)

    #plt.subplots_adjust(left = None, bottom = None, right = None, top= None, wspace = None, hspace = 0.8)        
    plt.tight_layout()

class SingleRun:
    maxArea = 0
    maxT = 0
    def __init__(self, filename):   
        with open(filename, "r") as dat:
            while (line := dat.read()) != "":
                exec(line)

        if self.bladeArea > SingleRun.maxArea:
            SingleRun.maxArea = float(self.bladeArea)
        if self.tAxis[-1] > SingleRun.maxT:
            SingleRun.maxT = float(self.tAxis[-1])


    def plot(self):
        self.tAxis[-1] = SingleRun.maxT

        colour = (lambda area: ((self.bladeArea / SingleRun.maxArea), 0, 1-(self.bladeArea / SingleRun.maxArea)))(self.bladeArea)
                
        GlobalAxes.axVelocity.plot(self.tAxis, self.vzAxis, color = (colour))
        GlobalAxes.axAngularV.plot(self.tAxis, self.vthetaAxis, color = (colour))
        GlobalAxes.axAcceleration.plot(self.tAxis, self.azAxis, color = (colour))
        GlobalAxes.axAngularA.plot(self.tAxis, self.athetaAxis, color = (colour))
        #GlobalAxes.axBladeAngle.plot(self.tAxis, self.bladeAngleAxis, color = (colour))

        GlobalAxes.axTerminalVWid.plot(self.bladeWid, self.vzAxis[-1], ".", color = (colour))
        GlobalAxes.axTerminalVLen.plot(self.bladeLen, self.vzAxis[-1], ".", color = (colour))
        GlobalAxes.axTerminalThetaWid.plot(self.bladeWid, self.vthetaAxis[-1], ".", color = (colour))
        GlobalAxes.axTerminalThetaLen.plot(self.bladeLen, self.vthetaAxis[-1], ".", color = (colour))

##        GlobalAxes.axColourKey.plot(0, self.bladeArea, ".", color = colour)

runs = [SingleRun("data\\" + file) for file in os.listdir("data")]
[run.plot() for run in runs]

plt.show()
