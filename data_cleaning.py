import pandas as pd
import re

# Converts a race time string to total seconds
def convert_time_to_seconds(mark):
    
    if mark == 'NT' or pd.isna(mark):
        return None  # No Time
    try:
        if ':' in mark:
            minutes, seconds = mark.split(':')
            return int(minutes) * 60 + float(seconds)
        else:
            return float(mark)  # For marks like '52.34' (seconds only)
    except:
        return None

# Extracts date from the Meet_Info column
def extract_date_from_meet_info(meet_info):
    try:
        match = re.search(r'([A-Za-z]{3,9}\s\d{1,2}(?:-\s?\d{1,2})?,?\s\d{4})', meet_info)
        if match:
            date_str = match.group(1)
            # Handle date ranges like 'Apr 17-18, 2025' → pick the first day
            date_str = date_str.replace('-', ' ').split()[0:2] + [date_str.split()[-1]]
            date_cleaned = ' '.join(date_str)
            return pd.to_datetime(date_cleaned, errors='coerce')
        else:
            return pd.NaT
    except:
        return pd.NaT

# Extracts the numeric placement from Place column
def extract_placement(place):
    match = re.match(r'(\d+)', str(place))
    if match:
        return int(match.group(1))
    else:
        return None

# Cleans the scraped TFRRS DataFrame
def clean_tfrrs_data(df):
    df = df.copy()
    df['Race_Date'] = df['Meet_Info'].apply(extract_date_from_meet_info)
    df['Time_seconds'] = df['Mark'].apply(convert_time_to_seconds)
    df['Placement_Number'] = df['Place'].apply(extract_placement)
    return df
