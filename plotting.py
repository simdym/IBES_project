import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import heartpy_impl as hp
import ecg_detector_impl as ed
import neurokit2_impl as nk

def flip_signal(signal):
    mean = np.mean(signal)

    return 2*mean - signal

def plot_peaks(ax, peaks, data, color='red'):
    ax.plot(peaks, np.array(data)[peaks], '.', color=color)

df = pd.read_csv("simen_1.csv")

ppg_data = df['6']
ecg_data = df['5']

ppg_data -= np.mean(ppg_data) #Centers around 0
ecg_data -= np.mean(ecg_data) #Centers around 0

fig1, (ax1, ax2) = plt.subplots(2, 1)

sample_rate = 1000


"""#Filter plotting
from scipy import signal
fig2, ax = plt.subplots()
b, a = signal.iirnotch(w0=0.05, Q=0.05, fs=sample_rate)
freq, h = signal.freqz(b, a, fs=sample_rate)
ax.plot(freq, 20*np.log10(abs(h)), color='red', label='notch')
ax.set_xlim([0, 100])
ax.set_ylim([-25, 10])
ax.legend()"""

#PPG plotting:
filt_nk_ppg_data = nk.ppg_preprocess(ppg_data, sample_rate=sample_rate)
nk_ppg_peaks = nk.get_ppg_peaks(ppg_data, sample_rate=sample_rate)
plot_peaks(ax1, nk_ppg_peaks, filt_nk_ppg_data, 'darkgreen')

ax1.plot(ppg_data, label='raw')
ax1.plot(filt_nk_ppg_data, label='nk')


#ECG plotting:
filt_nk_ecg_data = nk.ecg_preprocess(ecg_data, sample_rate=sample_rate)
nk_ecg_peaks = nk.get_ecg_peaks(ecg_data, sample_rate=sample_rate)
plot_peaks(ax2, nk_ecg_peaks, filt_nk_ecg_data, 'darkgreen')

ax2.plot(ecg_data, label='raw')
ax2.plot(filt_nk_ecg_data, label='nk')

#PTT, heartbeat and blood pressure plotting
fig3, ax4 = plt.subplots()
ax4.plot(np.diff(nk_ecg_peaks), label='ecg_period', drawstyle='steps')
ax4.plot(np.diff(nk_ppg_peaks), label='ppg_period', drawstyle='steps')
ax4.plot(nk.get_ecg_heartrate(ecg_data, sample_rate), label='ecg_hr')
ax4.plot(nk.get_ppg_heartrate(ppg_data, sample_rate), label='ppg_hr')

ax4.plot(nk.get_ptt(nk_ecg_peaks, nk_ppg_peaks), label='ptt')


ax4.legend()
"""
ax4.plot(filt_nk_ppg_data, label='nk')
plot_peaks(ax4, nk_ecg_peaks, filt_nk_ecg_data, 'orange')

ax4.plot(filt_nk_ecg_data, label='nk')
plot_peaks(ax4, nk_ppg_peaks, filt_nk_ppg_data, 'darkgreen')"""
ax4.legend()

ax1.legend()
ax2.legend()
plt.show()