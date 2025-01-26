import pandas as pd
import neurokit2 as nk
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d
from datetime import datetime
from collections import defaultdict

df = pd.read_csv("C:\hackathon-uci\ml_model\Wakefulness\csv_outputs\subject1_ppg_data.csv", header=0, names=["time", "ppg", "score"])
time = df["time"].values
ppg = df["ppg"].values
# Convert time column to datetime format
# Extract PPG signal as a NumPy array
smoothed_data = gaussian_filter1d(ppg, sigma=2)
peaks, properties = find_peaks(smoothed_data, height=350, prominence=50)

print("Peaks found at indices:", peaks)
prev_time = time[0]
format = "%H:%M:%S.%f"
timeToHrvs = defaultdict(list)
for peak_idx in peaks:
    print("Time: " + str(time[peak_idx])) 
    print("Value: " + str(ppg[peak_idx])) 
    hour = time[peak_idx][:2]
    # Assume this gives the hour
    print(hour)
    cur_time = datetime.strptime(time[peak_idx], format)
    timeToHrvs[hour].append(cur_time - prev_time)
    prev_time = cur_time


# print(peaks)