# Author: Ebrahim Muneer
# Plot functions

import matplotlib.pyplot as plt

# Function for plotting the staLta function as well as thresholds (For debugging purposes)
def plot_staLta(tr_times, tr_data, predictedArrival, sta_lta, on_threshold, filename):

    plt.figure(figsize=(12, 6))
    
    plt.subplot(211)
    plt.plot(tr_times, tr_data)
    plt.xlim([min(tr_times), max(tr_times)])
    plt.title(f"{filename} - Seismic Data")
    plt.ylabel("Velocity (m/s)")
    plt.xlabel("Time (s)")
    plt.axvline(predictedArrival, color='red', linestyle='--', label="Predicted Arrival")
    plt.legend()
    
    plt.subplot(212)
    plt.plot(tr_times, sta_lta, color = 'orange')
    plt.xlim([min(tr_times), max(tr_times)])
    plt.axvline(predictedArrival, color='red', linestyle='--', label="Predicted Arrival")
    plt.axhline(on_threshold, color='blue', linestyle='--', label="On Threshold")
    plt.title("STA/LTA Ratio")
    plt.ylabel("STA/LTA Ratio")
    plt.xlabel("Time (s)")
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# Plotting the seismic data along with the "start of event" line
def plot_trace(tr_times, tr_data, seismic_start, filename):
    plt.figure(figsize=(12, 6))
    plt.plot(tr_times, tr_data)
    plt.axvline(seismic_start, color='red', linestyle='-', label="Predicted Start")
    plt.title(f"{filename}")
    plt.ylabel("Velocity (m/s)")
    plt.xlabel("Time (s)")
    plt.legend()
    plt.tight_layout()
    plt.show()
