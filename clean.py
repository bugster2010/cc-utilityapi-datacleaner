import pandas as pd
from datetime import datetime
from datetime import timedelta

# 1 week of 15 min interval
entries_per_week = 672 

# allowed amount of created data. Should expect about 4 per year
created_error_max = 16

testfile = "assets/csv/raw.csv"

class DataCleaningError(Exception):
    pass

def removeDiscrepencies(df, annual):

    # Check for missing column names, throw error if any are missing
    required_columns = ['interval_start', 'interval_end', 'interval_kWh', 'fwd_kWh', 'net_kWh']
    missing_columns = set(required_columns) - set(df.columns)
    
    if missing_columns:
        raise DataCleaningError('Missing columns: {}'.format(', '.join(missing_columns)))
    
    #preparing data for cleaning
    df = reverseDF(df)
    if(annual):
        df = makeCalendarYear(df, 'interval_start')

    # Convert the 'interval_start' and 'interval_end' columns to datetime objects
    df['interval_start'] = pd.to_datetime(df['interval_start'], format='%m/%d/%Y %H:%M', errors='coerce')
    df['interval_end'] = pd.to_datetime(df['interval_end'], format='%m/%d/%Y %H:%M', errors='coerce')

    
    #new dataframe we will create and return
    cleanDF = []


    
    #setting data
    currHighestTime = datetime(year=1,month=1,day=1,hour=0,minute=0,second=0)
    df.reset_index()
    
        
    #begin for loop for iteration through data
    #index is given the int of the index and row is the data
    print("Removing time discrepencies")
    for index, row in df.iterrows():
        prev = index - 1
        cleanRow = row

        #validate start time is 15 minutes from end time
        if(annual):
            timeDifference = row['interval_end'].replace(year=2000) - row['interval_start'].replace(year=2000)
        else:
            timeDifference = row['interval_end'] - row['interval_start']
        if(timeDifference != timedelta(minutes = 15)):
            #fix to the proper time difference
            print("Improper start end time fixing")
            print("Previous Time: ", cleanRow['interval_end'], cleanRow['interval_start'])
            cleanRow['interval_end'] = row['interval_start'] + timedelta(minutes = 15)
            print("Correction:", cleanRow['interval_start'], cleanRow['interval_end'])
            print()
            
        if(annual):
            currHighestTest = cleanRow['interval_start'].replace(year=2000)
        else:
            currHighestTest = cleanRow['interval_start']

        skipped = 0
        #validate there is no repeat
        if(currHighestTest < currHighestTime):
            #this effectively skips anything that starts before what we have already deemed has ended 
            print(currHighestTest, ' was skipped')
            skipped = skipped + 1
            if(skipped > error_max):
                raise DataCleaningError('Skipped data has breached the cleaning error maximum')
            continue

        currHighestTime = cleanRow['interval_end']

        if(annual):
            currHighestTime = currHighestTime.replace(year = 2000)


        #validate all times exist
        if(len(cleanDF)>= 1):

            if(annual):
                verifyTimeBool = cleanDF[-1].interval_end.replace(year=2000) != cleanRow['interval_start'].replace(year=2000)
            else:
                verifyTimeBool = cleanDF[-1].interval_end != cleanRow['interval_start']
            
            if(verifyTimeBool):
                #if it is greater then fill in a blank
                #use a week ago to fill in the blank, otherwise use a week forward
                #inverted due to reversed indexing
                if(0<= (index - entries_per_week) <= len(df.index)):

                    copyInd = index - entries_per_week + 1
                    print("Fetching Week Prior")

                else:

                    print("Fetching Week Forward")
                    copyInd = index + entries_per_week + 1
                
                
                copyIntervalStart = cleanDF[-1].interval_end
                copyIntervalEnd = row['interval_start']
                print("Creating Copied data between", copyIntervalStart, "and", copyIntervalEnd)

                #used as a dual clause for the while loop
                if(annual):
                    intervalWhileClause = copyIntervalEnd.replace(year=2000) != copyIntervalStart.replace(year=2000)
                else:
                    intervalWhileClause = copyIntervalEnd != copyIntervalStart

                #used for error checking purposes
                intervalsCopied = 0

                while(intervalWhileClause):
                    
                    copy_curr = df.loc[copyInd].copy()

                    print("Copied data from:", df.loc[copyInd].interval_start, df.loc[copyInd].interval_end)
                    copy_curr.interval_start = copyIntervalStart.strftime('%m/%d/%Y %H:%M')
                    copy_curr.interval_end = (copyIntervalStart + timedelta(minutes = 15)).strftime('%m/%d/%Y %H:%M')
                
                    copyIntervalStart += timedelta(minutes=15)
                    cleanDF.append(copy_curr)
                    copyInd += 1

                    intervalsCopied = intervalsCopied + 1

                    if(intervalsCopied > created_error_max):
                        raise DataCleaningError('Maximum created data reached. Check that you have sufficient data if annual is selected')

                    if(annual):
                        intervalWhileClause = copyIntervalEnd.replace(year=2000) != copyIntervalStart.replace(year=2000)
                    else:
                        intervalWhileClause = copyIntervalEnd != copyIntervalStart
                    
        

        cleanDF.append(cleanRow)
    print("Completed time corrections")

    print()
    print("Beginning Removing Zero Values")
    cleanDF = removeZeroVals(pd.DataFrame(cleanDF))
    print("Completed")


    return cleanDF




def reverseDF(df):
    # reverses the dataframe
    df = df[::-1]
    return df
    
def verifyData(df):
    required_columns = ['interval_start', 'interval_end']
    missing_columns = set(required_columns) - set(df.columns)
    
    if missing_columns:
        raise DataCleaningError('Missing columns: {}'.format(', '.join(missing_columns)))
    df['interval_start'] = pd.to_datetime(df['interval_start'], format='%m/%d/%Y %H:%M', errors='coerce')
    df['interval_end'] = pd.to_datetime(df['interval_end'], format='%m/%d/%Y %H:%M', errors='coerce')
    flag = True
    
    prevEnd = None
    counter = 0
    for index, row in df.iterrows():
        if(row['interval_kWh'] == 0 and row['fwd_kWh'] == 0 and row['net_kWh'] == 0):
            print("Zero Discrepency Detected at start time: ", row['interval_start'])
            flag = False
        if(prevEnd != None):
            if(prevEnd != row['interval_start'] and prevEnd - row['interval_start']!= timedelta(days = 365)):

                print("Discrepency Detected. End:", prevEnd, "is not equal to", row['interval_start'])

                #if it's a year apart then it's our wrap date
                flag = False

        if(row['interval_end'] - row['interval_start'] != timedelta(minutes=15)):
            print("Discrepency Detected. Start time", row['interval_start'], "is not 15 minutes from", row['interval_end'])
            flag = False
        prevEnd = row['interval_end']
    return flag

#Testing script from early development
def testScript():
    data = pd.read_csv(testfile)
    data = removeDiscrepencies(data)
    data.to_csv("assets/csv/testfile.csv")

#run function for use by the frontend. Takes a CSV and a Boolean
def runCleaner(file, annual):
    data = pd.read_csv(file)
    data = removeDiscrepencies(data, annual)

    if(not verifyData(data)):
        raise DataCleaningError('Data not Properly Cleaned')


    cleanData = data.to_csv(index=False)

    return cleanData


#takes the data and sorts it into one calendar year from January -> December. "The Wrapper"
def makeCalendarYear(df, dateColumn):
    # Ensure only 1 calendar year
    df[dateColumn] = pd.to_datetime(df[dateColumn])

    most_recent_date = df[dateColumn].max()

    # Calculate the start date (one year prior to the most recent date)
    start_date = most_recent_date - pd.DateOffset(years=1)

    df = df.sort_values(dateColumn, ascending=False)

    # Filter the DataFrame to include only dates within the calendar year
    df = df[df[dateColumn] >= start_date]

    # Sort the remaining year
    df['sortingColumn'] = pd.to_datetime(df[dateColumn], errors='coerce')
    df['newSortingColumn'] = df['sortingColumn'].dt.strftime('%m/%d %H:%M')

    df = df.sort_values(by='newSortingColumn')

    df = df.drop(['sortingColumn', 'newSortingColumn'], axis=1)

    return df


#removes the zero values from our dataframe
def removeZeroVals(df):

    currIndex = 0
    copyIndex = -1

    df = df.reset_index()
    for index, row in df.iterrows():
        
        #verifies to grab from week ahead or week before
        if(currIndex < entries_per_week):
            copyIndex = index + entries_per_week

        else:
            copyIndex = index - entries_per_week

        if(row['interval_kWh'] == 0 and row['fwd_kWh'] == 0 and row['net_kWh'] == 0):

            #this is for edge cases looking forward before the zeroes have been removed, if it is a zero a week ahead it jumps another week forward. Should be minimal
            while(df.loc[copyIndex].interval_kWh == 0 and df.loc[copyIndex].fwd_kWh == 0 and df.loc[copyIndex].net_kWh == 0):
                print("Edge case in removing zero values. Jumping forward an extra week for data fetching")
                copyIndex = copyIndex + entries_per_week

            #Replaces zero values from desired week
            print("Zero detected, copying from start time:", df.loc[copyIndex].interval_start, "for: ", row['interval_start'])
            df.at[index, 'interval_kWh'] = df.loc[copyIndex].interval_kWh
            df.at[index, 'fwd_kWh'] = df.loc[copyIndex].fwd_kWh
            df.at[index, 'net_kWh'] = df.loc[copyIndex].net_kWh

        currIndex = currIndex + 1

    return df


