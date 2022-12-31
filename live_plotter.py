import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import neurokit2_impl as nk



class live_plotter:
    def animate(self, i):
        self.data = np.append(self.data, self.bitalino.read(self.nSamples), axis=0)
        self.ax.clear()
        if(self.plot_type == 'raw'):
            self.plot_raw(6)
        elif(self.plot_type == 'ecg_hr'):
            self.plot_ecg_hr()
        elif (self.plot_type == 'ppg_hr'):
            self.plot_ppg_hr()
        elif(self.plot_type == 'ptt'):
            self.plot_ptt()
        elif(self.plot_type == 'bp'):
            self.plot_bp()

    #Plotting functions
    def plot_raw(self, channel):
        self.ax.plot(self.data[:, channel][-self.display_len:], label=str(channel))
        self.ax.legend(loc=2, prop={'size': 6})

    def plot_ecg_hr(self):
        data = self.data[:, 5][-self.display_len:]

        if len(data) >= self.display_len:
            hr = nk.get_ecg_heartrate(data, self.sample_rate)

            self.res.append(np.mean(hr))
            self.ax.plot(self.res[-self.display_len:])

    def plot_ppg_hr(self):
        data = self.data[:, 6][-self.display_len:]
        if len(data) >= self.display_len:
            hr = nk.get_ppg_heartrate(data, self.sample_rate)

            self.res.append(np.mean(hr))
            self.ax.plot(self.res[-self.display_len:])

    def plot_ptt(self):
        ecg_data = self.data[:, 5][-self.display_len:]
        ppg_data = self.data[:, 6][-self.display_len:]
        if len(ecg_data) >= self.display_len:
            ptt = nk.get_ptt(ecg_data, ppg_data, self.sample_rate)

            self.res.append(np.mean(ptt))
            self.ax.plot(self.res[-self.display_len:])

    def plot_bp(self):
        ecg_data = self.data[:, 5][-self.display_len:]
        ppg_data = self.data[:, 6][-self.display_len:]
        if len(ecg_data) >= self.display_len:
            bp = nk.get_blood_pressure(ecg_data, ppg_data, self.sample_rate)

            self.res.append(np.mean(bp))
            self.ax.plot(self.res[-self.display_len:])

    def __init__(self, bitalino, channels, nSamples, display_len=10, window_len=1000, sample_rate=1000, plot_type='raw'):
        """

        :param bitalino: bitalino device
        :param channels: bitalino channels
        :param nSamples: samples per reading from bitaling
        :param window_len: amount of samples displayed
        :param sample_rate
        :param plot_type: plotting type ('raw', 'pulse', 'freq')
        """
        self.bitalino = bitalino
        self.channels = channels
        self.nSamples = nSamples
        self.display_len = display_len
        self.window_len = window_len
        self.sample_rate = sample_rate
        self.plot_type = plot_type
        self.data = bitalino.read(0)

        self.res = [] #[[] for _ in range(6)]

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

        df = pd.read_csv("titouan_1.csv")
        self.data = df.to_numpy()

    def inc_x(self, num):
        self.x=(num+self.x)%len(self.data)

    def read(self, num):
        reading = self.data[self.x:self.x+num]
        self.inc_x(num)
        return reading

    def stop(self):
        pass
