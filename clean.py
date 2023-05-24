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

    
    df = reverseDF(df)

    # Convert the 'interval_start' and 'interval_end' columns to datetime objects
    df['interval_start'] = pd.to_datetime(df['interval_start'], format='%m/%d/%Y %H:%M', errors='coerce')
    df['interval_end'] = pd.to_datetime(df['interval_end'], format='%m/%d/%Y %H:%M', errors='coerce')

    cleanDF = []


    #begin for loop for iteration through data
    #index is given the int of the index and row is the data
    #set the lowest time possible
    currHighestTime = datetime(year=1,month=1,day=1,hour=0,minute=0,second=0)
    
    flag = 0
    for index, row in df.iterrows():

        prev = index - 1
        cleanRow = row
        

        #validate start time is 15 minutes from end time
        timeDifference = row['interval_end'] - row['interval_start']
        if(timeDifference != timedelta(minutes = 15)):
            #fix to the proper time difference
            print(cleanRow['interval_end'], cleanRow['interval_start'])
            cleanRow['interval_end'] = row['interval_start'] + timedelta(minutes = 15)
            print(cleanRow['interval_end'], cleanRow['interval_start'])
            print(cleanDF[-1].interval_start, cleanDF[-1].interval_end, cleanRow['interval_start'], cleanRow['interval_end'])
            flag = 2
            
            
        
        #validate there is no repeat
        if(cleanRow['interval_start'] < currHighestTime):
            #this effectively skips anything that starts before what we have already deemed has ended 
            continue

        currHighestTime = cleanRow['interval_end']

        if(flag != 0):
                print("flag tripped:", cleanDF[-1].interval_end, cleanRow['interval_start'])
                print(cleanDF[-1].interval_end != cleanRow['interval_start'])
                flag = flag - 1

        #validate all times exist
        if(len(cleanDF)>= 1):

            if(cleanDF[-1].interval_end != cleanRow['interval_start']):
                #if it is greater then fill in a blank
                #use a week ago to fill in the blank, otherwise use a week forward
                if(0<= (index - entries_per_week) <= len(df.index)):
                    copyInd = index - entries_per_week
                    print("Fetching Week Prior")
                else:
                    print("Fetching Week Forward")
                    copyInd = index + entries_per_week
                
                copyIntervalStart = cleanDF[-1].interval_end
                copyIntervalEnd = row['interval_start']
                print("Creating Copied data between", copyIntervalStart, "and", copyIntervalEnd)


                while(copyIntervalEnd != copyIntervalStart):
                    
                    copyInd += 1
                    
                    copy_curr = df.iloc[copyInd].copy()
                    copy_curr.interval_start = copyIntervalStart.strftime('%Y-%m-%d %H:%M:%S')
                    copy_curr.interval_end = (copyIntervalStart + timedelta(minutes = 15)).strftime('%Y-%m-%d %H:%M:%S')
                
                    copyIntervalStart += timedelta(minutes=15)
                    cleanDF.append(copy_curr)
                    
        
        cleanDF.append(cleanRow)

        


    
    

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