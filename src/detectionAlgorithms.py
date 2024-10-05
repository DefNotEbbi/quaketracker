# Author: Ebrahim Muneer
# Algorithms to detect the start of a seismic event

import numpy as np
from obspy.signal.trigger import trigger_onset, recursive_sta_lta, classic_sta_lta, z_detect
from plot import plot_staLta

# The recursiveStaLtaMax algorithm
# Uses the recursice staLta algorithm and the trigger_onset func from obspy
# Detects all possible peak starts and chooses the one closest to the graph's maximum
# Lowest Error: 2.73%
def recursiveStaLtaMax(tr_times, tr_data, sampling_rate, short_window=155, long_window=1470, on_factor=0.3):
    sta_lta = recursive_sta_lta(tr_data, int(short_window * sampling_rate), int(long_window * sampling_rate))
    
    on_threshold = np.mean(sta_lta) + (np.std(sta_lta) * on_factor)
    off_threshold = on_threshold * 0.999

    onsets = trigger_onset(sta_lta, on_threshold, off_threshold)
    
    maxStaLtaIndex = np.argmax(sta_lta)
    max_index = np.argmax(np.abs(tr_data))

    forceSta = False
    staDiff = abs(maxStaLtaIndex - max_index)
    if staDiff < 1000:
        forceSta = True

    dif = len(tr_data)
    selected_peak = None

    if len(onsets) > 0:
        for i in range(len(onsets)):

            if forceSta and onsets[i][0] < maxStaLtaIndex:
                dif = abs(onsets[i][0] - maxStaLtaIndex)
                selected_peak = i
                continue


            if abs(onsets[i][0] - max_index) < dif and onsets[i][0] < max_index:
                dif = abs(onsets[i][0] - max_index)
                selected_peak = i
                continue

        if selected_peak is not None:
            event_start_sample = onsets[selected_peak][0]
        else:
            print("Warning: No peak found before maximum")
            for i in range(len(onsets)):
                if abs(onsets[i][0] - max_index) < dif:
                    dif = abs(onsets[i][0] - max_index)
                    selected_peak = i
            if selected_peak is not None:
                event_start_sample = onsets[selected_peak][0]

        return tr_times[event_start_sample], sta_lta, on_threshold
    else:
        return tr_times[0], sta_lta, on_threshold

# The classicStaLtaMax algorithm
# Uses the classic staLta algorithm and the trigger_onset func from obspy
# Detects all possible peak starts and chooses the one closest to the graph's maximum
# Lowest Error: 2.94%
def classicStaLtaMax(tr_times, tr_data, sampling_rate, short_window=155, long_window=1470, on_factor=0.3):
    sta_lta = classic_sta_lta(tr_data, int(short_window * sampling_rate), int(long_window * sampling_rate))
    
    on_threshold = np.mean(sta_lta) + (np.std(sta_lta) * on_factor)
    off_threshold = on_threshold * 0.999

    onsets = trigger_onset(sta_lta, on_threshold, off_threshold)
    
    maxStaLtaIndex = np.argmax(sta_lta)
    max_index = np.argmax(np.abs(tr_data))

    forceSta = False
    staDiff = abs(maxStaLtaIndex - max_index)
    if staDiff < 1000:
        forceSta = True

    dif = len(tr_data)
    selected_peak = None

    if len(onsets) > 0:
        for i in range(len(onsets)):

            if forceSta and onsets[i][0] < maxStaLtaIndex:
                dif = abs(onsets[i][0] - maxStaLtaIndex)
                selected_peak = i
                continue


            if abs(onsets[i][0] - max_index) < dif and onsets[i][0] < max_index:
                dif = abs(onsets[i][0] - max_index)
                selected_peak = i
                continue

        if selected_peak is not None:
            event_start_sample = onsets[selected_peak][0]
        else:
            print("Warning: No peak found before maximum")
            for i in range(len(onsets)):
                if abs(onsets[i][0] - max_index) < dif:
                    dif = abs(onsets[i][0] - max_index)
                    selected_peak = i
            if selected_peak is not None:
                event_start_sample = onsets[selected_peak][0]

        return tr_times[event_start_sample], sta_lta, on_threshold
    else:
        return tr_times[0], sta_lta, on_threshold

# Z-Detect
# Uses the z-detect algorithm and the trigger_onset func from obspy
# Detects all possible peak starts and chooses the one closest to the graph's maximum
# Lowest Error: 2.94% at window 260
def zDetect(tr_times, tr_data, sampling_rate, short_window=260, on_factor=0.3):
    sta_lta = z_detect(tr_data, int(short_window * sampling_rate))
    
    on_threshold = np.mean(sta_lta) + (np.std(sta_lta) * on_factor)
    off_threshold = on_threshold * 0.999

    onsets = trigger_onset(sta_lta, on_threshold, off_threshold)
    
    maxStaLtaIndex = np.argmax(sta_lta)
    max_index = np.argmax(np.abs(tr_data))

    forceSta = False
    staDiff = abs(maxStaLtaIndex - max_index)
    if staDiff < 1000:
        forceSta = True

    dif = len(tr_data)
    selected_peak = None

    if len(onsets) > 0:
        for i in range(len(onsets)):

            if forceSta and onsets[i][0] < maxStaLtaIndex:
                dif = abs(onsets[i][0] - maxStaLtaIndex)
                selected_peak = i
                continue


            if abs(onsets[i][0] - max_index) < dif and onsets[i][0] < max_index:
                dif = abs(onsets[i][0] - max_index)
                selected_peak = i
                continue

        if selected_peak is not None:
            event_start_sample = onsets[selected_peak][0]
        else:
            print("Warning: No peak found before maximum")
            for i in range(len(onsets)):
                if abs(onsets[i][0] - max_index) < dif:
                    dif = abs(onsets[i][0] - max_index)
                    selected_peak = i
            if selected_peak is not None:
                event_start_sample = onsets[selected_peak][0]

        return tr_times[event_start_sample], sta_lta, on_threshold
    else:
        return tr_times[0], sta_lta, on_threshold


# The maxDetect algorithm (deciprated)
# Detects the absolute peak of the trace
# Keeps going one index backwards until the previous index (to the left) is larger than the current one
# Or until the threshold is reached
# Lowest Error: 2.62% on jump window 293
def maxDetect(tr_times, tr_data, jumpWindow = 290):
    max_index = np.argmax(np.abs(tr_data))
    if tr_data[max_index] > 0:
        tr_data = np.abs(tr_data / tr_data[max_index])

    val1 = np.abs(tr_data[max_index])
    val2 = np.abs(tr_data[max_index - jumpWindow])
    index = max_index - jumpWindow


    threshold = np.mean(np.abs(tr_data))
    while val2 < val1 or val2 > threshold:
        index -= jumpWindow
        val1 = val2
        val2 = np.abs(tr_data[index])

    return tr_times[index]

# Maps a curve to the absolute values of the data
# Gets the maximum and goes backwards till it reaches the mean
# Error: 24.62%
def maxLineMap(tr_times, tr_data, degree=5):

    tr_data = np.abs(tr_data)
    mean = np.mean(tr_data)
    max_index = np.argmax(tr_data)

    x = np.arange(len(tr_data))
    coeffs = np.polyfit(x, tr_data, degree)
    tr_data = np.polyval(coeffs, x)

    a = max_index

    while tr_data[a] > mean:
        a -= 1

    return tr_times[a], tr_data

# Returns the maximum of the absolute value of the data
# Error: 3.44%
def simpleMaxAlgo(tr_times, tr_data):
    max_index = np.argmax(np.abs(tr_data))
    return tr_times[max_index]

if __name__ == "__main__":
    print("Hello, World!")
