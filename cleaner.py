import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta

# 1 week of 15 min interval
entries_per_week = 672 

class DataCleaningError(Exception):
    pass

def to_datetime(date_string):
    # Try parsing the string using the '%m/%d/%Y %H:%M' format first
    try:
        date_obj = datetime.strptime(date_string, '%m/%d/%Y %H:%M')
    except ValueError:
        # If that fails, try using the '%Y-%m-%d %H:%M:%S' format
        try:
            date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # If that fails, raise a DataCleaningError exception
            raise DataCleaningError(f"Could not convert {date_string} to datetime")
    return date_obj


def create_clean_dataframe(df):

    # Check for missing column names, throw error if any are missing
    required_columns = ['interval_start', 'interval_end']
    missing_columns = set(required_columns) - set(df.columns)
    
    if missing_columns:
        raise DataCleaningError('Missing columns: {}'.format(', '.join(missing_columns)))


    cleaned_data = []
    
    for ind in df.index:

        # Store variables for current index of dataframe
        interval_start = to_datetime(df['interval_start'][ind])
        interval_end = to_datetime(df['interval_end'][ind])
        _timedelta = interval_end - interval_start
        
        if (_timedelta == timedelta(minutes = 15)):
            # proper entry, no modification need
            cleaned_data.append(df.iloc[ind])
        else:
            # There is data missing in this set at the current index
            # Will copy usage data from week prior for most-accurate fix
            
            copy_index = ind - entries_per_week
            ph_interval_end = interval_end
            
            while (ph_interval_end - interval_start >= timedelta(minutes = 15)):
                copy_curr = df.iloc[copy_index].copy()
                copy_curr.interval_end = ph_interval_end.strftime('%m/%d/%Y %H:%M')
                copy_curr.interval_start = (ph_interval_end - timedelta(minutes = 15)).strftime('%m/%d/%Y %H:%M')
                
                cleaned_data.append(copy_curr)
                
                ph_interval_end = ph_interval_end - timedelta(minutes = 15)

    cleaned_df = pd.DataFrame(cleaned_data)

    print('completed data cleaning')
    
    return cleaned_df
