# Given json of SDNN, RMSSD, pNN50, 
# Source for bpm: https://pmc.ncbi.nlm.nih.gov/articles/PMC6592896/#Fig1
# Source for SDNN: https://journals.lww.com/nsca-jscr/abstract/2007/02000/heart_rate_variability_in_elite_american.41.aspx
hrv_data = {
    "SDNN": {
        "male": {"value": 70.115, "std_dev": 28.03},
        "female": {"value": 70.897, "std_dev": 29.13}
    },
    "RMSSD": {
        "male": {"value": 71.437, "std_dev": 35.99},
        "female": {"value": 77.431, "std_dev": 35.82}
    },
    "PNN50": {
        "male": {"value": 19.782, "std_dev": 9.46},
        "female": {"value": 23.172, "std_dev": 10.27}
    },
    "BPM": {
        "male": {"value": 79.1, "std_dev": 14.5},
        "female": {"value": 79.1, "std_dev": 14.5}
    }
}
