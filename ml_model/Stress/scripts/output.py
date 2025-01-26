import csv
from datetime import datetime, timedelta
from collections import defaultdict
# Path to the CSV file
csv_file_path = r"C:\Users\dtro1\Downloads\WESAD\WESAD\S2\S2_E4_Data\IBI.csv"
ground_truth_file_path = r"C:\Users\dtro1\Downloads\WESAD\WESAD\S2\S2_quest.csv"
# Function to convert elapsed time (seconds) to human-readable time, returns a string
def convert_to_human_time(elapsed_time):
    # Starting reference time (initial timestamp)
    reference_time = datetime.fromtimestamp(1495437325.000000)  # Original timestamp
    # Add elapsed time as a timedelta
    new_time = reference_time + timedelta(seconds=elapsed_time)
    
    # Calculate the total elapsed time in minutes and seconds
    elapsed_minutes = elapsed_time // 60
    elapsed_seconds = int(elapsed_time % 60)
    # Return the elapsed time in "minutes:seconds" format
    return f"{int(elapsed_minutes):02}:{elapsed_seconds:02}"
# Open the CSV file and read its contents


# Function to extract the start and end times for Base and TSST
# Returns a dictionary of dictionaries
def extract_start_end_times(file_path):
    # Initialize a dictionary to store the start and end times
    times = {
        'Base': {'start': None, 'end': None},
        'TSST': {'start': None, 'end': None}
    }

    # Open the file and read line by line
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Loop through each line to find relevant data
        for line in lines:
            # Check for the START and END lines
            if line.startswith('# START'):
                start_times = line.strip().split(';')[1:-1]  # Skip the first empty part and last part
                times['Base']['start'] = float(start_times[0])
                times['TSST']['start'] = float(start_times[1])
            elif line.startswith('# END'):
                end_times = line.strip().split(';')[1:-1]  # Skip the first empty part and last part
                times['Base']['end'] = float(end_times[0])
                times['TSST']['end'] = float(end_times[1])

    return times
def extract_minutes_seconds(time_str):
    # Split the time string into minutes and seconds based on the colon
    minutes, seconds = time_str.split(":")
    # Convert the minutes and seconds to integers
    minutes = int(minutes)
    seconds = int(seconds)
    
    return minutes, seconds


# {'Base': {'start': 7.08, 'end': 26.32}, 'TSST': {'start': 39.55, 'end': 50.3}}

score_to_hrv = defaultdict(list) # {1: [hrv1, hrv2, etc]}
begin_end_dict = extract_start_end_times(ground_truth_file_path)
base_start = begin_end_dict["Base"]["start"]
base_end = begin_end_dict["Base"]["end"]
stress_start = begin_end_dict["TSST"]["start"]
stress_end = begin_end_dict["TSST"]["end"]

time_to_classification_base = []
time_to_classification_stress = []

with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header if there is one
    for row in reader:
        elapsed_time = float(row[0])  # Assuming elapsed time is in the first column
        value = row[1]  # The corresponding value (e.g., IBI) in the second column
        human_time = convert_to_human_time(elapsed_time)
        minutes, seconds = extract_minutes_seconds(human_time)
        minutes, seconds = str(minutes), str(seconds)
        dec_time = minutes + "." + seconds
        dec_time = float(dec_time)
        print(dec_time)
        if base_start <= dec_time <= base_end:
            # Store
            time_to_classification_base.append({"time": dec_time, "value": value, "classification": 0})
        elif stress_start <= dec_time <= stress_end:
            time_to_classification_stress.append({"time": dec_time, "value": value, "classification": 1})

with open("output1.csv", mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['time', 'value', 'classification'])
    writer.writeheader()  # Write the header row
    writer.writerows(time_to_classification_base)  # Write the data rows

with open("output2.csv", mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['time', 'value', 'classification'])
    writer.writeheader()  # Write the header row
    writer.writerows(time_to_classification_stress)  # Write the data rows
# print(extract_start_end_times(ground_truth_file_path))  