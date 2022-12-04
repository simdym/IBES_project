import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ecgdetectors import Detectors
ecg = Detectors(1000)


class live_plotter:
    def calculate_fft(self, data):
        detrended_data = sig.detrend(data[-self.window_len:])
        filter = sig.butter(N=20, Wn=[0.5, 4], btype="bandpass", output="sos", fs=1000)
        filtered_data = sig.sosfilt(filter, detrended_data)
        windowed_data = filtered_data * np.hamming(min(len(data), self.window_len))
        return np.abs(np.fft.fft(windowed_data))

    def calculate_snr(self, data):
        detrended_data = sig.detrend(data[-self.window_len:])
        windowed_data = detrended_data * np.hamming(min(len(data), self.window_len))
        fft = np.abs(np.fft.fft(windowed_data))
        var = np.var(detrended_data)
        return 10*np.log10(max(fft)/var)

    def animate(self, i):
        self.data = np.append(self.data, self.bitalino.read(self.nSamples), axis=0)
        self.ax.clear()
        if(self.plot_type == 'raw'):
            self.plot_raw()
        elif(self.plot_type == 'hr'):
            self.plot_hr()
        elif(self.plot_type == 'peaks'):
            self.plot_peaks()
        elif(self.plot_type == 'detrend'):
            self.plot_detrend()
        elif (self.plot_type == 'fft'):
            self.plot_fft()
        elif(self.plot_type == 'freq'):
            self.plot_freq()
        elif (self.plot_type == 'pulse'):
            self.plot_pulse()
        elif(self.plot_type == 'snr'):
            self.plot_snr()

    def plot_raw(self):
        for channel in self.channels:
            self.ax.plot(self.data[:, channel][-self.display_len:], label=str(channel))
            self.ax.legend(loc=2, prop={'size': 6})

    def plot_hr(self):
        for channel in self.channels:
            r_peaks = ecg.hamilton_detector(self.data[:, channel][-self.window_len:])
            hp = np.diff(r_peaks)
            hr = np.average(1 / hp)
            print(r_peaks)
            print(hp)

            self.res[channel].append(hr*1000*60)
            self.ax.plot(self.res[channel][-self.display_len:])

    def plot_peaks(self):
        self.plot_raw()
        for channel in self.channels:
            r_peaks = ecg.engzee_detector(self.data[:, channel][-self.display_len:])
            peaks = np.zeros(self.display_len)
            peaks[r_peaks] = 100
            self.ax.plot(peaks, label=str(channel))
            self.ax.legend(loc=2, prop={'size': 6})


    def plot_detrend(self):
        for channel in self.channels:
            self.ax.plot(sig.detrend(self.data[:, channel][-self.display_len:]), label=str(channel))
            self.ax.legend(loc=2, prop={'size': 6})

    def plot_fft(self):
        for channel in self.channels:
            fft = self.calculate_fft(self.data[:, channel][-self.window_len:])
            fftfreq = np.fft.fftfreq(len(fft), 1/1000)

            fftfreq = fftfreq[fftfreq >= 0]
            fft = fft[:len(fftfreq)]

            self.ax.plot(fftfreq, fft, label=str(channel))
            plt.xlim(0, 5)
            self.ax.legend(loc=2, prop={'size': 6})

    def plot_freq(self):
        for channel in self.channels:
            fft = self.calculate_fft(self.data[:, channel][-self.window_len:])
            freq_ind = np.argmax(fft)
            fftfreq = np.fft.fftfreq(len(fft), 1 / 1000)

            self.res[channel].append(np.abs(fftfreq[freq_ind]))
            self.ax.plot(self.res[channel][-self.display_len:])

    def plot_pulse(self):
        for channel in self.channels:
            fft = self.calculate_fft(self.data[:, channel][-self.window_len:])
            freq_ind = np.argmax(fft)
            fftfreq = np.fft.fftfreq(len(fft), 1 / 1000)

            self.res[channel].append(60 * np.abs(fftfreq[freq_ind]))
            self.ax.plot(self.res[channel][-self.display_len:])

    def plot_snr(self):
        for channel in self.channels:
            snr = self.calculate_snr(self.data[:, channel][-self.window_len:])
            self.res[channel].append(snr)
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

    def __del__(self):
        self.bitalino.stop()
        self.bitalino.close()

class mock_dev:
    """
    Mock device class for testing of plotting without Bitalino
    """
    def __init__(self):
        self.freq_seed = 0
        self.x = 0

    def read(self, num):
        import numpy as np
        import time

        a = 1
        b = 1
        Fs = 1000

        chance = 0.01

        freq = 0.25 #2 * np.pi * np.cos(0.01 * self.freq_seed)
        self.freq_seed+=int((1 - chance) < np.random.rand())

        x = np.arange(self.x, self.x + num)
        self.x += num

        time.sleep(0.1)
        return np.transpose(np.tile(np.sin(freq * (x + b * np.random.normal(size=num))) + 500 + a * np.random.normal(size=num), (6,1)))
