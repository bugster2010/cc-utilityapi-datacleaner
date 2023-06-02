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

    df = makeCalendarYear(df, 'interval_start')

    # Convert the 'interval_start' and 'interval_end' columns to datetime objects
    df['interval_start'] = pd.to_datetime(df['interval_start'], format='%m/%d/%Y %H:%M', errors='coerce')
    df['interval_end'] = pd.to_datetime(df['interval_end'], format='%m/%d/%Y %H:%M', errors='coerce')

    # save the current year in it's own column
    #df['Saved Year'] = df['interval_start'].dt.year

    

    cleanDF = []


    #begin for loop for iteration through data
    #index is given the int of the index and row is the data
    #set the lowest time possible
    currHighestTime = datetime(year=1,month=1,day=1,hour=0,minute=0,second=0)
    
    flag = 0

    df.reset_index()
    #for index, row in df.iterrows():
    #   df.at[index, 'interval_end'] = row['interval_end'].replace(year=2000)
    #    df.at[index, 'interval_start'] = row['interval_start'].replace(year=2000)
        
        

    for index, row in df.iterrows():
        prev = index - 1
        cleanRow = row

        #validate start time is 15 minutes from end time
        timeDifference = row['interval_end'].replace(year=2000) - row['interval_start'].replace(year=2000)
        if(timeDifference != timedelta(minutes = 15)):
            #fix to the proper time difference
            print("Improper start end time fixing")
            print("Previous Time: ", cleanRow['interval_end'], cleanRow['interval_start'])
            cleanRow['interval_end'] = row['interval_start'] + timedelta(minutes = 15)
            print("Correction:", cleanRow['interval_start'], cleanRow['interval_end'])
            print()
            
            
        currHighestTest = cleanRow['interval_start'].replace(year=2000)

        #validate there is no repeat
        if(currHighestTest < currHighestTime):
            #this effectively skips anything that starts before what we have already deemed has ended 
            print(currHighestTest, ' was skipped')
            continue

        currHighestTime = cleanRow['interval_end']
        currHighestTime = currHighestTime.replace(year = 2000)


        #validate all times exist
        if(len(cleanDF)>= 1):

            if(cleanDF[-1].interval_end.replace(year=2000) != cleanRow['interval_start'].replace(year=2000)):
                #if it is greater then fill in a blank
                #use a week ago to fill in the blank, otherwise use a week forward
                #inverted due to reversed indexing
                if(0<= (index - entries_per_week) <= len(df.index)):

                    copyInd = index - entries_per_week
                    print("Fetching Week Prior")

                else:

                    print("Fetching Week Forward")
                    copyInd = index + entries_per_week
                
                
                copyIntervalStart = cleanDF[-1].interval_end
                copyIntervalEnd = row['interval_start']
                print("Creating Copied data between", copyIntervalStart, "and", copyIntervalEnd)


                while(copyIntervalEnd.replace(year=2000) != copyIntervalStart.replace(year=2000)):
                    
                    
                    copy_curr = df.iloc[copyInd].copy()

                    print("Copied data from:", df.iloc[copyInd].interval_start, df.iloc[copyInd].interval_end)
                    copy_curr.interval_start = copyIntervalStart.strftime('%m/%d/%Y %H:%M')
                    copy_curr.interval_end = (copyIntervalStart + timedelta(minutes = 15)).strftime('%m/%d/%Y %H:%M')
                
                    copyIntervalStart += timedelta(minutes=15)
                    cleanDF.append(copy_curr)
                    copyInd += 1
                    
        
        cleanDF.append(cleanRow)



    return pd.DataFrame(cleanDF)




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

def testScript():
    data = pd.read_csv(testfile)
    data = removeDiscrepencies(data)
    data.to_csv("assets/csv/testfile.csv")

def runCleaner(file):
    data = pd.read_csv(file)
    data = removeDiscrepencies(data)

    verifyData(data)

    #if(not verifyData(data)):
    #    raise DataCleaningError('Data not Properly Cleaned')

    #if(reverse):
    #    data = reverseDF(data)


    cleanData = data.to_csv(index=False)

    return cleanData


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



#idea for calendar fixing, reimplement indexing using pandas drop index. Will have to reimplement the week copying method if we do that