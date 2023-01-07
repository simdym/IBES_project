import numpy as np
import neurokit2 as nk
import ProjectModels as bp  # Blood pressure models

"""
    Implementations of functions using the neurokit2 library
"""

def ecg_preprocess(data, sample_rate):
    data = data - np.mean(data)
    return nk.ecg_clean(data, sampling_rate=sample_rate, method="neurokit")


def ppg_preprocess(data, sample_rate):
    data = data - np.mean(data)
    return nk.ppg_clean(data, sampling_rate=sample_rate, method='elgendi')


def get_ecg_peaks(data, sample_rate):
    data_proccesed = ecg_preprocess(data, sample_rate)
    rpeaks = nk.ecg_findpeaks(data_proccesed, sampling_rate=sample_rate)['ECG_R_Peaks']

    return rpeaks


def get_ppg_peaks(data, sample_rate):
    data_proccesed = ppg_preprocess(data, sample_rate)
    speaks = nk.ppg_findpeaks(data_proccesed, sampling_rate=sample_rate)['PPG_Peaks']

    return speaks

def get_ptt(ecg_peaks, ppg_peaks):
    ppt = []
    for i in range(len(ecg_peaks)):
        ppg_peak = ppg_peaks[ppg_peaks > ecg_peaks[i]]  # Finds next ppg_peak
        if len(ppg_peak) > 0:
            ppg_peak = ppg_peak[0]
            if i < len(ecg_peaks) - 1:
                if ppg_peak < ecg_peaks[i + 1]:  # Only uses ppg_peak if peak is located before next ecg_peak
                    ppt.append(ppg_peak-ecg_peaks[i])
    return ppt

def get_ecg_heartrate(data, sample_rate):
    peaks = get_ecg_peaks(data, sample_rate)

    return sample_rate*60/np.diff(peaks)

def get_mean_ecg_heartrate(data, period, sample_rate):
    peaks = get_ecg_peaks(data, sample_rate)

    sample_period = int(period * sample_rate)
    diff_peaks_mean = []
    for peak in peaks[sample_period < peaks]:
        peaks_in_period = peaks[peaks <= peak]
        peaks_in_period = peaks_in_period[(peak - sample_period) < peaks_in_period]
        diff_peaks_mean.append(np.mean(np.diff(peaks_in_period)))
    print(diff_peaks_mean)
    return sample_rate * 60 / np.array(diff_peaks_mean)

def get_ppg_heartrate(data, sample_rate):
    peaks = get_ppg_peaks(data, sample_rate)

    return sample_rate*60/np.diff(peaks)

def get_mean_ppg_heartrate(data, period, sample_rate):
    peaks = get_ppg_peaks(data, sample_rate)

    sample_period = int(period * sample_rate)
    diff_peaks_mean = []
    for peak in peaks[sample_period < peaks]:
        peaks_in_period = peaks[peaks <= peak]
        peaks_in_period = peaks_in_period[(peak - sample_period) < peaks_in_period]
        diff_peaks_mean.append(np.mean(np.diff(peaks_in_period)))
    print(diff_peaks_mean)
    return sample_rate * 60 / np.array(diff_peaks_mean)

def get_Geshe_blood_pressure(ecg_data, ppg_data, height, sample_rate):
    ecg_peaks = get_ecg_peaks(ecg_data, sample_rate)
    ppg_peaks = get_ppg_peaks(ppg_data, sample_rate)
    ptt = get_ptt(ecg_peaks, ppg_peaks)

    import scipy.ndimage as nd

    kernel_size = 9
    ptt = nd.median_filter(ptt, kernel_size)

    blood_pressure = bp.Gesche(0.5, height, ptt)

    return blood_pressure

def get_MoenAndKorteweg_blood_pressure(ecg_data, ppg_data, height, sample_rate):
    ecg_peaks = get_ecg_peaks(ecg_data, sample_rate)
    ppg_peaks = get_ppg_peaks(ppg_data, sample_rate)
    ptt = get_ptt(ecg_peaks, ppg_peaks)

    import scipy.ndimage as nd

    kernel_size = 9
    ptt = nd.median_filter(ptt, kernel_size)

    blood_pressure = bp.MoenAndKorteweg(height, ptt)

    return blood_pressure
