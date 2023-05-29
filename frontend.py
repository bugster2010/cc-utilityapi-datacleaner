from PIL import Image
import pandas as pd
import os
import sys

from clean import *
import streamlit as st
# import shutil
# from tkinter import Tk, filedialog
# from pathlib import Path

def main():
    moduleInterface()
    


def moduleInterface():
    st.set_page_config(page_title="UtilityAPI Cleaner", layout="wide")
    #default values
    clean_file = None
    image = Image.open('assets/logo.png')

    st.image(image, width=700)
    st.title("UtilityAPI Data Cleaner")
    

    inputColumn, outputColumn = st.columns(2)
    # File input
    with inputColumn:
        st.header("Select Input CSV")
        selected_file = st.file_uploader("Upload a file")


        #reverse = st.checkbox("Reverse Data", value=False)
            # Button to start cleaning program
        if st.button("Clean Data"):
            if selected_file is None:
                  st.error("Please select an input file.")
            else:
                 clean_file = runCleaner(selected_file)
                 
                 st.success("File Cleaned Successfully")
        
        

    with outputColumn:
        if(clean_file != None):
            # Download button
            st.header("Download File")
            
            st.download_button(
                label="Download data as CSV",
                data=clean_file,
                file_name='clean_' + selected_file.name,
                mime='text/csv',
            )

    st.text("Copyright Clean Coalition")

if __name__ == "__main__":
    main()
