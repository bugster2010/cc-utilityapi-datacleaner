import pandas as pd
from datetime import datetime
from datetime import timedelta

# 1 week of 15 min interval
entries_per_week = 672 

testfile = "assets/csv/AACI_Health_Center_raw_data.csv"

class DataCleaningError(Exception):
    pass

def removeDiscrepencies(df):
    
    # Reverse the dataset so it is in order
    df = reverseDF(df)
    


    return df




def reverseDF(df):
    # reverses the dataframe
    df = df[::-1]
    return df
    


def testScript():
    data = pd.read_csv(testfile)
    data = removeDiscrepencies(data)
    data.to_csv("assets/csv/testfile.csv")

testScript()