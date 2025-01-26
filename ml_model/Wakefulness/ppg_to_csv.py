import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d
from collections import defaultdict
import datetime
import csv
import neurokit2 as nk

def extract_csv_data_pandas(file_path):
    df = pd.read_csv(file_path)
    return df

# Obtain data from annotations.csv, returns list of tuples (time, score)
def obtain_annotation_times(file_path):
    df = extract_csv_data_pandas(file_path)
    times = df["Datetime"].values
    event = df["Event"].values
    sss_scores = df["Value"].values

    annotation_time_score = []
    for i in range(len(times)):
        if event[i] == "Stanford Sleepiness Self-Assessment (1-7)":
            annotation_time_score.append((times[i], sss_scores[i]))
    return annotation_time_score 

# Function takes in annotation times of one subject and returns a dict mapping csv to a list of hours
# annotation_time_score = (time, sleepyscore)
def select_csv(annotation_time_score, first_csv_path, second_csv_path):
    # Times start at 13:00 on 1/1, go to 23:59 on 1/1
    # Times start at roughly 0:05 and go to 11:00.
    csv_to_times = defaultdict(list) # Maps csv to all the times
    for idx in range(len(annotation_time_score)):
        time = annotation_time_score[idx][0]
        # time is a string
        if idx == 0 or idx == 1:
            continue
        date = time[0:10]
        hour = time[11:] + ".000000"
        if date == "2000-01-01":
            csv_to_times[first_csv_path].append(hour)
        elif date == "2000-01-02":
            csv_to_times[second_csv_path].append(hour)
    return csv_to_times

# Given a time array and ppg array, returns (time, peaks) data. Not sure what this will return yet.
def obtain_peaks(time, ppg):
    peaksDict = defaultdict(list) # {time: [], ppg: []}
    smoothed_data = gaussian_filter1d(ppg, sigma=2)
    # Peaks holds indices of...peaks
    peaks, properties = find_peaks(smoothed_data, height=350, prominence=50)
    # TODO: Figure out what this should return.

# Function should grab x amount of samples, starting at each of the given times (or closest). 
# Pass in csv_to_times = {csvpath: [times]}
# and time_sss [(annotation_time, score)]
def grab_n_samples(num_samples, csv_to_times, time_sss):
    # grab all samples from 1st csv
    csv_data = defaultdict(list) # {time, ppg, score}
    for key, value in csv_to_times.items():
        path = key
        ppg_df = extract_csv_data_pandas(path)
        # For each annotation reading
        for annotation_time in value:
            annotation_time = datetime.datetime.strptime(annotation_time, "%H:%M:%S.%f").time()
            valid_idx_start = 0
            valid_idx_end = 0
            # For each line in the csv file
            for i in range(len(ppg_df)):
                time = ppg_df.iloc[i, 0]
                ppg_val = ppg_df.iloc[i, 1]
                temp_time = datetime.datetime.strptime(time, "%H:%M:%S.%f").time()
                # Locate the first valid time index
                if temp_time > annotation_time:
                    valid_idx_start = i
                    valid_idx_end = i + num_samples
                    break
            # Find the sleep score for this bin
            score = 0
            for t, val in time_sss:
                    t = t[11:] + ".000000"
                    t =  datetime.datetime.strptime(t, "%H:%M:%S.%f").time()
                    if annotation_time == t:
                        #// revisit score
                        score = val
                        break

            # Grab n entries from csv a
            for idx in range(valid_idx_start, valid_idx_end):
                time = ppg_df.iloc[idx, 0]
                ppg_val = ppg_df.iloc[idx, 1]
                csv_data["time"].append(time)
                csv_data["ppg"].append(ppg_val)
                csv_data["score"].append(score)
                # print("adding" + time + " " + str(ppg_val))

            # # Contains n samples from the annotation time.
            # time = []
            # ppg = []
            # for idx in range(valid_idx_start, valid_idx_end):
            #     time.append(ppg_df.iloc[idx, 0])
            #     ppg.append(ppg_df.iloc[idx, 1])
            # obtain_peaks(time, ppg)
            # # Map the score to every single entry

    rows = [
        {"time": time, "ppg": ppg, "score": score}
        for time, ppg, score in zip(csv_data["time"], csv_data["ppg"], csv_data["score"])
    ]

    with open("output.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["time", "ppg", "score"])
        writer.writeheader()
        writer.writerows(rows)

                    





annotation_path = "C:\hackathon-uci\ml_model\Wakefulness\data\gamer1-annotations.csv"

annotation_time_score = obtain_annotation_times(annotation_path)
csv_to_times = select_csv(annotation_time_score, 
                          "C:\hackathon-uci\ml_model\Wakefulness\data\gamer1-ppg-2000-01-01.csv", 
                          "C:\hackathon-uci\ml_model\Wakefulness\data\gamer1-ppg-2000-01-02.csv")
grab_n_samples(300, csv_to_times, annotation_time_score)



# Prints out peaks 
# file_path = 'C:\MSWE\Wakefulness\ppg_sample.csv'

# df = extract_csv_data_pandas(file_path)
# # Convert pandas series into np array
# time = df["time"].values
# ppg = df["ppg"].values

# smoothed_data = gaussian_filter1d(ppg, sigma=2)
# peaks, properties = find_peaks(smoothed_data, height=350, prominence=50)

# print("Peaks found at indices:", peaks)
# for peak_idx in peaks:
#     print("Time: " + str(time[peak_idx])) 
#     print("Value: " + str(ppg[peak_idx])) 

# print(peaks)