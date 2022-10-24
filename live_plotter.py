import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate(i, bitalino, ax, ys, channel, nSamples):
    data = bitalino.read(nSamples)[:, channel]
    print(data)
    for d in data:
        ys.append(d)

    ax.clear()
    ax.plot(ys)

def live_plotter(bitalino, channel, nSamples):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ys = []

    ani = animation.FuncAnimation(fig, animate, fargs=(bitalino, ax, ys, channel, nSamples), interval=1000)
    plt.show()

