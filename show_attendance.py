import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return
            
        subject_dir = f"Attendance/{Subject}"
        
        # Check if subject directory exists
        if not os.path.exists(subject_dir):
            t = f'No attendance records found for subject: {Subject}'
            text_to_speech(t)
            messagebox.showerror("Error", f"No attendance records found for {Subject}. Please check the subject name.")
            return
            
        # Change directory and get CSV files
        os.chdir(subject_dir)
        filenames = glob(f"{Subject}*.csv")
        
        # Check if any CSV files exist
        if not filenames:
            t = f'No attendance sheets found for subject: {Subject}'
            text_to_speech(t)
            messagebox.showerror("Error", f"No attendance sheets found for {Subject}.")
            return
            
        try:
            # Read all CSV files
            df = [pd.read_csv(f) for f in filenames]
            newdf = df[0]
            
            # Merge all dataframes if there are multiple files
            for i in range(1, len(df)):
                newdf = newdf.merge(df[i], how="outer")
                
            # Replace NaN with 0 for attendance calculation
            newdf.fillna(0, inplace=True)
            
            # Initialize attendance column
            newdf["Attendance"] = '0%'
            
            # Calculate attendance percentage
            for i in range(len(newdf)):
                try:
                    # Get all columns except Enrollment, Name, and Attendance
                    attendance_cols = newdf.columns[2:-1]
                    # Calculate mean only for numeric columns
                    attendance_values = pd.to_numeric(newdf.iloc[i][attendance_cols], errors='coerce')
                    mean_attendance = attendance_values.mean()
                    
                    # Handle NaN mean value
                    if pd.isna(mean_attendance):
                        percentage = 0
                    else:
                        percentage = int(round(mean_attendance * 100))
                    
                    newdf.at[i, "Attendance"] = f"{percentage}%"
                except Exception as e:
                    print(f"Error calculating attendance for row {i}: {str(e)}")
                    newdf.at[i, "Attendance"] = "0%"
            
            # Save the consolidated attendance
            newdf.to_csv("attendance.csv", index=False)

            # Create attendance display window
            root = tkinter.Tk()
            root.title("Attendance of " + Subject)
            root.configure(background="black")
            
            # Read and display the attendance data
            with open("attendance.csv") as file:
                reader = csv.reader(file)
                r = 0
                for col in reader:
                    c = 0
                    for row in col:
                        # Adjust column width based on content
                        width = max(len(str(row)) + 2, 10)
                        label = tkinter.Label(
                            root,
                            width=width,
                            height=1,
                            fg="yellow",
                            font=("times", 15, " bold "),
                            bg="black",
                            text=row,
                            relief=tkinter.RIDGE,
                        )
                        label.grid(row=r, column=c)
                        c += 1
                    r += 1
            root.mainloop()
            
        except Exception as e:
            t = f'Error processing attendance: {str(e)}'
            text_to_speech(t)
            messagebox.showerror("Error", f"Error processing attendance: {str(e)}")
            return

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            subject_dir = f"Attendance/{sub}"
            if os.path.exists(subject_dir):
                os.startfile(subject_dir)
            else:
                t = f'Directory not found for subject: {sub}'
                text_to_speech(t)
                messagebox.showerror("Error", f"No directory found for subject: {sub}")

    # Create the subject window
    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    
    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="white",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="white",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="white",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="black",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="black",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()