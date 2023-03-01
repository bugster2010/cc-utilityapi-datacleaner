import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import pandas as pd

# Set up the GUI
root = tk.Tk()
root.title("Clean Coalition CSV Tool")
root.geometry("500x600")
root.configure(bg="#0072C6")
root.resizable(False, False)

# Add Clean Coalition logo and name
logo_image = Image.open("clean_coalition_logo.png")
width, height = logo_image.size
aspect_ratio = height / width
new_width = 350
new_height = int(new_width * aspect_ratio)
logo_image = logo_image.resize((new_width, new_height), Image.LANCZOS)
logo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo, bg="#0072C6")
logo_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Function to upload CSV file
def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        df = pd.read_csv(file_path)
        process_data(df)

# Function to save cleaned CSV data
def save_file(df):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if file_path:
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Export Complete", "Data cleaned and saved successfully!")
        
# Function to process CSV data
def process_data(df):
    # Replace NaN values with 0
    df.fillna(0, inplace=True)
    
    # Perform some other cleaning tasks...
    
    # Display results
    save_button = tk.Button(root, text="Export Cleaned Data", command=lambda: save_file(df), font=("Arial", 16), bg="#FFFFFF")
    save_button.grid(row=3, column=0, pady=10, padx=10, columnspan=2)
    result_label = tk.Label(root, text="Data processed!", font=("Arial", 16), bg="#0072C6", fg="#FFFFFF")
    result_label.grid(row=2, column=1, pady=10)

# Add Upload CSV button
upload_button = tk.Button(root, text="Upload CSV", command=upload_file, font=("Arial", 16), bg="#FFFFFF")
upload_button.grid(row=1, column=0, pady=10, padx=10, columnspan=2)

# Center the Upload CSV button under the logo
logo_label.grid_rowconfigure(1, weight=1)
upload_button.grid(row=2, column=0, pady=10, columnspan=2)

# Add info button
def show_info():
    messagebox.showinfo("Clean Coalition CSV Tool", "This program cleans and exports UtilityAPI CSV files with date/time discrepancies typically occurring during daylight savings.\n\nPlease select a CSV file to upload \n\nThe program will clean it up and export the cleaned data.\n\n© 2023 Clean Coalition. All rights reserved.")

info_button = tk.Button(root, text="About", command=show_info, font=("Arial", 16), bg="#FFFFFF")
info_button.grid(row=1, column=0, pady=10, padx=10, sticky="e")

# Add copyright text
copyright_label = tk.Label(root, text="© 2023 Clean Coalition. All rights reserved.", font=("Arial", 10), bg="#0072C6", fg="#FFFFFF")
copyright_label.grid(row=5, column=0, columnspan=2)

# Center the logo, button, and copyright on the page
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the GUI
root.mainloop()
