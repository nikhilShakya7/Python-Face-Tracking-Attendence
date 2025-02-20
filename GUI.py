# main_gui.py
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import subprocess
from addStudent import open_add_student  # Import the function from add_student.py

VENV_PYTHON = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")  # Windows

# Function to run face recognition script
def run_face_recognition():
    subprocess.run([VENV_PYTHON, "main.py"])

# Function to view attendance file
def view_attendance():
    try:
        subprocess.run(["notepad.exe", "attendance.csv"])  # Opens CSV in Notepad
    except FileNotFoundError:
        messagebox.showerror("Error", "Attendance file not found.")

# Create the main window
root = tk.Tk()
root.title("Face Attendance System")
root.geometry("640x480")
root.configure(bg="#0096FF")

# Custom Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 14), padding=10, background="#4CAF50", foreground="black")
style.configure("Title.TLabel", font=("Arial", 18, "bold"), background="#f4f4f4", foreground="#333")

# Title Label
title_label = ttk.Label(root, text="Face Attendance System", style="Title.TLabel")
title_label.pack(pady=20)

# Buttons
take_attendance_btn = ttk.Button(root, text="Take Attendance", command=run_face_recognition)
take_attendance_btn.pack(pady=15, ipadx=20)

view_attendance_btn = ttk.Button(root, text="View Attendance", command=view_attendance)
view_attendance_btn.pack(pady=15, ipadx=20)

# Add Student Button
add_student_btn = ttk.Button(root, text="Add Student", command=lambda: open_add_student(root))
add_student_btn.pack(pady=15, ipadx=20)

# Run the GUI
root.mainloop()

