import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class live_plotter:
    def animate(self, i):
        self.data = np.append(self.data, self.bitalino.read(self.nSamples), axis=0)
        print(self.data.shape)
        self.ax.clear()
        for channel in self.channels:
            print(channel, self.data[:, channel].shape)
            self.ax.plot(self.data[:, channel])

    def __init__(self, bitalino, channels, nSamples):
        self.bitalino = bitalino
        self.channels = channels
        self.nSamples = nSamples
        self.data = bitalino.read(self.nSamples)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)
        plt.show()

