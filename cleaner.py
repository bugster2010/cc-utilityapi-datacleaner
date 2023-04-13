import pandas as pd
from datetime import datetime
from datetime import timedelta

# 1 week of 15 min interval
entries_per_week = 672 

class DataCleaningError(Exception):
    pass

def create_clean_dataframe(df):
    # Check for missing column names, throw error if any are missing
    required_columns = ['interval_start', 'interval_end']
    missing_columns = set(required_columns) - set(df.columns)
    
    if missing_columns:
        raise DataCleaningError('Missing columns: {}'.format(', '.join(missing_columns)))

    # Convert the 'interval_start' and 'interval_end' columns to datetime objects
    df['interval_start'] = pd.to_datetime(df['interval_start'], format='%m/%d/%Y %H:%M', errors='coerce')
    df['interval_end'] = pd.to_datetime(df['interval_end'], format='%m/%d/%Y %H:%M', errors='coerce')

    cleaned_data = []
    
    for ind, row in df.iterrows():
        interval_start = row['interval_start']
        interval_end = row['interval_end']
        _timedelta = interval_end - interval_start
        
        if (_timedelta == timedelta(minutes = 15)):
            # proper entry, no modification need
            cleaned_data.append(row)
        else:
            # There is data missing in this set at the current index
            # Will copy usage data from week prior for most-accurate fix
            
            copy_index = ind - entries_per_week
            ph_interval_end = interval_end
            
            while (ph_interval_end - interval_start >= timedelta(minutes = 15)):
                copy_curr = df.iloc[copy_index].copy()
                copy_curr.interval_end = ph_interval_end.strftime('%Y-%m-%d %H:%M:%S')
                copy_curr.interval_start = (ph_interval_end - timedelta(minutes = 15)).strftime('%Y-%m-%d %H:%M:%S')
                
                cleaned_data.append(copy_curr)
                
                ph_interval_end = ph_interval_end - timedelta(minutes = 15)

    cleaned_df = pd.DataFrame(cleaned_data)

    print('completed data cleaning')
    
    return cleaned_df
