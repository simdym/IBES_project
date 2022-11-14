import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class live_plotter:
    def calculate_fft(self, data):
        detrended_data = sig.detrend(data[-self.window_len:])
        windowed_data = detrended_data * np.hamming(min(len(data), self.window_len))
        return np.abs(np.fft.fft(windowed_data))

    def animate(self, i):
        self.data = np.append(self.data, self.bitalino.read(self.nSamples), axis=0)
        self.ax.clear()
        if(self.plot_type == 'raw'):
            self.plot_raw()
        elif (self.plot_type == 'fft'):
            self.plot_fft()
        elif(self.plot_type == 'freq'):
            self.plot_freq()
        elif (self.plot_type == 'pulse'):
            self.plot_pulse()

    def plot_raw(self):
        for channel in self.channels:
            self.ax.plot(self.data[:, channel][-self.display_len:], label=str(channel))
            self.ax.legend(loc=2, prop={'size': 6})

    def plot_fft(self):
        for channel in self.channels:
            fft = self.calculate_fft(self.data[:, channel][-self.window_len:])
            fftfreq = np.fft.fftfreq(len(fft))

            fftfreq = fftfreq[fftfreq >= 0]
            fft = fft[:len(fftfreq)]

            self.ax.plot(fftfreq, fft, label=str(channel))
            self.ax.legend(loc=2, prop={'size': 6})

    def plot_freq(self):
        for channel in self.channels:
            fft = self.calculate_fft(self.data[:, channel][-self.window_len:])
            freq_ind = np.argmax(fft)
            self.res[channel].append(np.abs(np.fft.fftfreq(self.window_len, 1/1000)[freq_ind]))
            self.ax.plot(self.res[channel][-self.display_len:])

    def plot_pulse(self):
        for channel in self.channels:
            fft = self.calculate_fft(self.data[:, channel][-self.window_len:])
            freq_ind = np.argmax(fft)
            self.res[channel].append(60 * np.abs(np.fft.fftfreq(self.window_len, 1/1000)[freq_ind]))
            self.ax.plot(self.res[channel][-self.display_len:])

    def __init__(self, bitalino, channels, nSamples, display_len=10, window_len=1000, plot_type='raw'):
        """

        :param bitalino: bitalino device
        :param channels: bitalino channels
        :param nSamples: samples per reading from bitaling
        :param window_len: amount of samples displayed
        :param plot_type: plotting type ('raw', 'pulse', 'freq')
        """
        self.bitalino = bitalino
        self.channels = channels
        self.nSamples = nSamples
        self.window_len = window_len
        self.display_len = display_len
        self.plot_type = plot_type
        self.data = bitalino.read(0)

        self.res = [[] for _ in range(6)]

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

        ani = animation.FuncAnimation(self.fig, self.animate, interval=1)
        plt.show()

class mock_dev:
    """
    Mock device class for testing of plotting without Bitalino
    """
    def __init__(self):
        self.freq_seed = 0

    def read(self, num):
        import numpy as np
        import time

        a = 5
        b = 1

        freq = np.cos(0.01 * self.freq_seed)
        self.freq_seed+=1

        x = np.arange(num)
        time.sleep(0.1)
        return np.transpose(np.tile(np.sin(freq * (x + b * np.random.rand(num))) + 500 + a * np.random.rand(num), (6,1)))
