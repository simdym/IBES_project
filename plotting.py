import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import pandas as pd
import numpy as np
import neurokit2_impl as nk

#Signal slice
start = 2000
end = 8000

def flip_signal(signal):
    mean = np.mean(signal)

    return 2*mean - signal

def plot_peaks(ax, peaks, data, color='red'):
    peaks = peaks[peaks < end]
    peaks = peaks[peaks >= start]

    ax.plot(peaks/1000, np.array(data)[peaks], 'x', color=color, label="Detected peaks")

def gliding_avg(data, len):
    return np.convolve(data, np.ones(len), mode='valid')/len

df = pd.read_csv("titouan_1.csv")

ppg_data = df['6']
ecg_data = df['5']

sample_rate = 1000

def plot_signal(data, label):
    fig, ax = plt.subplots()

    t = np.linspace(start/1000, end/1000, end-start)
    ax.plot(t, data[start:end], label=label)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f s'))
    ax.legend()
    return fig, ax


#Plot processing
#PPG
def plot_ppg_raw():
    plot_signal(ppg_data, "Raw PPG")

def plot_ppg_preprocessed():
    filt_nk_ppg_data = nk.ppg_preprocess(ppg_data, sample_rate=sample_rate)
    plot_signal(filt_nk_ppg_data, "Preprocessed PPG")

def plot_ppg_peaks():
    filt_nk_ppg_data = nk.ppg_preprocess(ppg_data, sample_rate=sample_rate)
    fig, ax = plot_signal(filt_nk_ppg_data, "Preprocessed PPG")
    plot_peaks(ax, nk.get_ppg_peaks(ppg_data, sample_rate), filt_nk_ppg_data)

#ECG
def plot_ecg_raw():
    plot_signal(ecg_data, "Raw ECG")

def plot_ecg_preprocessed():
    filt_nk_ecg_data = nk.ecg_preprocess(ecg_data, sample_rate=sample_rate)
    plot_signal(filt_nk_ecg_data, "Preprocessed ECG")

def plot_ecg_peaks():
    filt_nk_ecg_data = nk.ecg_preprocess(ecg_data, sample_rate=sample_rate)
    fig, ax = plot_signal(filt_nk_ecg_data, "Preprocessed ECG")
    plot_peaks(ax, nk.get_ecg_peaks(ecg_data, sample_rate), filt_nk_ecg_data)

def plot_ptt():
    ecg_peaks = nk.get_ecg_peaks(ecg_data, sample_rate)
    ppg_peaks = nk.get_ppg_peaks(ppg_data, sample_rate)

    ptt = nk.get_ptt(ecg_peaks, ppg_peaks)

    fig, ax = plt.subplots()

    ax.plot(ecg_peaks[:len(ptt)]/1000, ptt, label="PTT")
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f s'))
    ax.legend()

def plot_hr():
    ecg_peaks = nk.get_ecg_peaks(ecg_data, sample_rate)
    ecg_peaks = (ecg_peaks[1:] + ecg_peaks[:-1]) / 2
    ecg_peaks /= 1000

    ecg_hr = nk.get_ecg_heartrate(ecg_data, sample_rate)

    ppg_peaks = nk.get_ppg_peaks(ppg_data, sample_rate)
    ppg_peaks = (ppg_peaks[1:] + ppg_peaks[:-1]) / 2
    ppg_peaks /= 1000

    ppg_hr = nk.get_ppg_heartrate(ppg_data, sample_rate)

    fig, ax = plt.subplots()

    ax.plot(ecg_peaks, ecg_hr, label="ECG heartrate")
    ax.plot(ppg_peaks, ppg_hr, label="PPG heartrate")
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f s'))
    ax.legend()

"""

#PPG plotting:
filt_nk_ppg_data = nk.ppg_preprocess(ppg_data, sample_rate=sample_rate)
nk_ppg_peaks = nk.get_ppg_peaks(ppg_data, sample_rate=sample_rate)
plot_peaks(ax1, nk_ppg_peaks, filt_nk_ppg_data, 'red')




#ECG plotting:
filt_nk_ecg_data = nk.ecg_preprocess(ecg_data, sample_rate=sample_rate)
nk_ecg_peaks = nk.get_ecg_peaks(ecg_data, sample_rate=sample_rate)
plot_peaks(ax2, nk_ecg_peaks, filt_nk_ecg_data, 'red')

ax2.plot(ecg_data, label='raw')
ax2.plot(filt_nk_ecg_data, label='nk')

#PTT, heartbeat and blood pressure plotting
fig3, ax4 = plt.subplots()

avg_len = 10
avg_nk_ecg_peaks = gliding_avg(np.diff(nk_ecg_peaks), avg_len)
avg_nk_ppg_peaks = gliding_avg(np.diff(nk_ppg_peaks), avg_len)

ax4.plot(np.diff(nk_ecg_peaks), label='ecg_period')
ax4.plot(avg_nk_ecg_peaks, label='avg_ecg_period')
ax4.plot(np.diff(nk_ppg_peaks), label='ppg_period')
ax4.plot(avg_nk_ppg_peaks, label='avg_ppg_period')

avg_ecg_hr = gliding_avg(nk.get_ecg_heartrate(ecg_data, sample_rate), avg_len)
avg_ppg_hr = gliding_avg(nk.get_ecg_heartrate(ecg_data, sample_rate), avg_len)

ax4.plot(nk.get_ecg_heartrate(ecg_data, sample_rate), label='ecg_hr')
ax4.plot(avg_ecg_hr, label='avg_ecg_hr')
ax4.plot(nk.get_ppg_heartrate(ppg_data, sample_rate), label='ppg_hr')
ax4.plot(avg_ppg_hr, label='avg_ecg_hr')

ax4.plot(nk.get_ptt(nk_ecg_peaks, nk_ppg_peaks), label='ptt')


ax4.legend()

ax4.plot(filt_nk_ppg_data, label='nk')
plot_peaks(ax4, nk_ecg_peaks, filt_nk_ecg_data, 'orange')

ax4.plot(filt_nk_ecg_data, label='nk')
plot_peaks(ax4, nk_ppg_peaks, filt_nk_ppg_data, 'darkgreen')
ax4.legend()

ax1.legend()
ax2.legend()"""

plot_ptt()
plot_hr()
plt.show()

plot_ecg_peaks()
plot_ppg_peaks()
plt.show()

plot_ppg_raw()
#plot_ppg_preprocessed()
plot_ecg_raw()
plot_ecg_preprocessed()
plt.show()