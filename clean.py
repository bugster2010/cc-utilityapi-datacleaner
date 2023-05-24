import pandas as pd
from datetime import datetime
from datetime import timedelta

# 1 week of 15 min interval
entries_per_week = 672 

testfile = "assets/csv/raw.csv"

class DataCleaningError(Exception):
    pass

def removeDiscrepencies(df):

    # Check for missing column names, throw error if any are missing
    required_columns = ['interval_start', 'interval_end']
    missing_columns = set(required_columns) - set(df.columns)
    
    if missing_columns:
        raise DataCleaningError('Missing columns: {}'.format(', '.join(missing_columns)))

    
    

    # Convert the 'interval_start' and 'interval_end' columns to datetime objects
    df['interval_start'] = pd.to_datetime(df['interval_start'], format='%m/%d/%Y %H:%M', errors='coerce')
    df['interval_end'] = pd.to_datetime(df['interval_end'], format='%m/%d/%Y %H:%M', errors='coerce')

    cleanDF = []

    #begin for loop for iteration through data
    #index is given the int of the index and row is the data
    #set the lowest time possible
    currHighestTime = datetime(year=1,month=1,day=1,hour=0,minute=0,second=0)
    # Reverse the dataset so it is in order
    df = reverseDF(df)
    for index, row in df.iterrows():
        
        prev = index - 1

        #validate start time is 15 minutes from end time
        timeDifference = row['interval_end'] - row['interval_start']
        if(timeDifference != timedelta(minutes = 15)):
            #fix to the proper time difference
            print(row['interval_start'], row['interval_end'])
            row['interval_end'] = row['interval_start'] + timedelta(minutes = 15)
            print(row['interval_start'], row['interval_end'])
        
        #validate there is no repeat
        if(row['interval_start'] < currHighestTime):
            #this effectively skips anything that starts before what we have already deemed has ended 
            continue

        currHighestTime = row['interval_end']

        #validate all times exist
        if(0 <= prev <= len(df.index)):
            if(df.iloc[prev].interval_end != df.iloc[index].interval_start):

                #if it is greater then fill in a blank
                #if(df.iloc[prev, 'interval_end'] <= row['interval_start']): <- this should never happen
                    
                #use a week ago to fill in the blank, otherwise use a week forward
                if(0<= (index - entries_per_week) <= len(df.index)):
                    copyInd = index - entries_per_week
                    print(1)
                else:
                    print(2)
                    copyInd = index + entries_per_week
                
                copyIntervalStart = df.iloc[prev].interval_end
                copyIntervalEnd = row['interval_start']

                while(copyIntervalEnd != copyIntervalStart):
                    copyInd += 1
                    
                    copy_curr = df.iloc[copyInd].copy()
                    copy_curr.interval_start = copyIntervalStart.strftime('%Y-%m-%d %H:%M:%S')
                    copy_curr.interval_end = (copyIntervalStart + timedelta(minutes = 15)).strftime('%Y-%m-%d %H:%M:%S')
                
                    copyIntervalStart += timedelta(minutes=15)
                    cleanDF.append(copy_curr)
                    break
        
        cleanDF.append(row)
            

        


    
    

    return pd.DataFrame(cleanDF)




def reverseDF(df):
    # reverses the dataframe
    df = df[::-1]
    return df
    


def testScript():
    data = pd.read_csv(testfile)
    data = removeDiscrepencies(data)
    data.to_csv("assets/csv/testfile.csv")

testScript()