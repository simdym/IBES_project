import numpy as np
import pandas as pd
import neurokit2 as nk

"""
    Implementations of functions using the neurokit2 library
"""

def ecg_preprocess(data, sample_rate):
    return nk.ecg_clean(data, sampling_rate=sample_rate, method="neurokit")


def ppg_preprocess(data, sample_rate):
    return nk.ppg_clean(data, sampling_rate=sample_rate, method='elgendi')


def get_ecg_peaks(data, sample_rate):
    data_proccesed = ecg_preprocess(data, sample_rate)
    rpeaks = nk.ecg_findpeaks(data, sampling_rate=sample_rate)['ECG_R_Peaks']

    return rpeaks


def get_ppg_peaks(data, sample_rate):
    data_proccesed = ppg_preprocess(data, sample_rate)
    speaks = nk.ppg_findpeaks(data, sampling_rate=sample_rate)['PPG_Peaks']

    return speaks

def get_ptt(ecg_peaks, ppg_peaks):
    ppt = []
    for ecg_peak in ecg_peaks:
        ppg_peak = ppg_peaks[ppg_peaks > ecg_peak]
        if(len(ppg_peak) > 0):
            ppg_peak = ppg_peak[0]
            ppt.append(ppg_peak-ecg_peak)

    return ppt

def get_ecg_heartrate(data, sample_rate):
    peaks = get_ecg_peaks(data, sample_rate)

    return sample_rate*60/np.diff(peaks)

def get_ppg_heartrate(data, sample_rate):
    peaks = get_ppg_peaks(data, sample_rate)

    return sample_rate*60/np.diff(peaks)

def get_blood_pressure(ecg_data, ppg_data, sample_rate):
    ptt = get_ptt(ecg_data, ppg_data, sample_rate)

    blood_pressure = 0 #f(ptt) TODO implement blood pressure function
    # (PS: use numpy functions as ptt is a numpy.array)

    # I would prefer that blood_pressure is an np.array of same size as ptt
    return blood_pressure