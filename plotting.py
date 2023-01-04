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

meas = "titouan_1"

df = pd.read_csv(meas+".csv")
if meas == "titouan_1":
    height = 174
    start_bp = 108
    end_bp = 111
    ref_bp = [start_bp, end_bp]
    start_hr = 73
    end_hr = 67
    ref_hr = [start_hr, end_hr]
elif meas == "simen_1":
    height = 190
    start_bp = 124
    end_bp = 114
    ref_bp = [start_bp, end_bp]
    start_hr = 59
    end_hr = 67
    ref_hr = [start_hr, end_hr]

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

    ax.plot([0, 60], ref_hr, '--', label="Reference meassurment")
    ax.plot(ecg_peaks, ecg_hr, label="ECG heartrate")
    ax.plot(ppg_peaks, ppg_hr, label="PPG heartrate")
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f s'))
    ax.legend()

def plot_bp():
    ecg_peaks = nk.get_ecg_peaks(ecg_data, sample_rate)

    Gershe_bp = nk.get_Geshe_blood_pressure(ecg_data, ppg_data, height, sample_rate)
    MoenAndKorteweg_bp = nk.get_MoenAndKorteweg_blood_pressure(ecg_data, ppg_data, height, sample_rate)

    fig, ax = plt.subplots()

    ax.plot([0, 60], ref_bp, '--', label="Reference meassurment")
    ax.plot(ecg_peaks[:len(Gershe_bp)] / 1000, Gershe_bp, label="Gershe")
    ax.plot(ecg_peaks[:len(MoenAndKorteweg_bp)] / 1000, MoenAndKorteweg_bp, label="Moen and Korteweg")
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f s'))
    ax.legend()

plot_ptt()
plot_bp()
plot_hr()
plt.show()

plot_ppg_raw()
plot_ppg_preprocessed()
plot_ecg_raw()
plot_ecg_preprocessed()
plt.show()