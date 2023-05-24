import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import pandas as pd
import os
import sys

import cleaner  # Import the cleaner.py file

# Set up the GUI
root = tk.Tk()
root.title("Clean Coalition CSV Tool")
root.geometry("500x600")
root.configure(bg="#0072C6")
root.resizable(False, False)

file_label = None


def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename


# Add Clean Coalition logo and name
logo_image = Image.open(get_path("assets/logo.png"))
width, height = logo_image.size
aspect_ratio = height / width
new_width = 350
new_height = int(new_width * aspect_ratio)
logo_image = logo_image.resize((new_width, new_height), Image.LANCZOS)
logo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo, bg="#0072C6")
logo_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Function to show info about the program
def show_info():
    messagebox.showinfo("Clean Coalition CSV Tool", "This program cleans and exports UtilityAPI CSV files with date/time discrepancies typically occurring during daylight savings.\n\nPlease select a CSV file to upload \n\nThe program will clean it up and export the cleaned data.\n\n© 2023 Clean Coalition. All rights reserved.")

def limit_string(s, max_length=20):
    return s[:max_length] + "..." if len(s) > max_length else s

# Function to upload CSV file
def upload_file():
    global file_label

    file_path = filedialog.askopenfilename()

    # Check if there's a previous label and destroy it if it exists
    if file_label:
        file_label.destroy()

    file_label = tk.Label(root, text='file: ' + limit_string(os.path.basename(file_path)), font=("Arial", 16), bg="#0072C6", fg="#FFFFFF")
    file_label.grid(row=6, column=0, sticky='W', padx=10)
    file_label.update()
    if file_path:
        df = pd.read_csv(file_path)
        process_data(df)


# Function to save cleaned CSV data
def save_file(df, reverse_option):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if file_path:
        if reverse_option.get() == "Reverse":
            df = df.iloc[::-1]
        df.to_csv(file_path, index=False)
        messagebox.showinfo(title="Export Complete", message="Data cleaned and saved successfully!")


# Function to process CSV data
def process_data(df):
    # Replace NaN values with 0
    df.fillna(0, inplace=True)

    # Create a new Toplevel window for the loading state
    loading_window = tk.Toplevel(root)
    loading_window.title("Processing Data")
    loading_window.geometry("250x100")
    loading_label = tk.Label(loading_window, text="Processing data, please wait...", font=("Arial", 12))
    loading_label.pack(pady=20)
    loading_window.update()  # Force update to display loading window

    # Use the cleaner module to clean the data
    df = cleaner.create_clean_dataframe(df)

    # Destroy the loading window and display the results
    loading_window.destroy()
    # Add a variable to store the selected option from the dropdown
    reverse_option = tk.StringVar(root)
    reverse_option.set("No Reverse")

    # Add a dropdown menu to select reverse option
    reverse_dropdown = tk.OptionMenu(root, reverse_option, "No Reverse", "Reverse")
    reverse_dropdown.config(font=("Arial", 12), bg="#FFFFFF")
    reverse_dropdown.grid(row=4, column=1)

    # Modify the save_button command to include the reverse_option variable
    save_button = tk.Button(root, text="Export Cleaned Data", command=lambda: save_file(df, reverse_option), font=("Arial", 16), bg="#FFFFFF")
    save_button.grid(row=4, column=0, pady=10, padx=10, columnspan=1)

# Add Upload CSV button
upload_button = tk.Button(root, text="Upload CSV", command=upload_file, font=("Arial", 16), bg="#FFFFFF")
upload_button.grid(row=2, column=1)

# Center the Upload CSV button under the logo
logo_label.grid_rowconfigure(1, weight=1)
upload_button.grid(row=2, column=0, pady=10, columnspan=2)

# Add copyright text
copyright_label = tk.Label(root, text="© 2023 Clean Coalition. All rights reserved.", font=("Arial", 10), bg="#0072C6", fg="#FFFFFF")
copyright_label.grid(row=7, column=0, columnspan=1)

# Add info button
info_button = tk.Button(root, text="About", command=show_info, font=("Arial", 16), bg="#FFFFFF")
info_button.grid(row=7, column=1, columnspan=1, pady=10)

# Center the logo, button, and copyright on the page
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the GUI
root.mainloop()

