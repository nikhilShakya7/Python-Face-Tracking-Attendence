import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import subprocess
import threading
from PIL import Image, ImageTk  # Import PIL for image handling

from addStudent import open_add_student
from removeStudent import remove_student

# Import the function from add_student.py

VENV_PYTHON = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")


# Function to run face recognition script
def run_face_recognition():
    subprocess.run([VENV_PYTHON, "main.py"])


def run_encode_generator():
    subprocess.run([VENV_PYTHON, "Encode-Generator.py"])


def take_attendance():
    threading.Thread(target=run_face_recognition, daemon=True).start()
    threading.Thread(target=run_encode_generator, daemon=True).start()


# Function to view attendance
def view_attendance():
    # Create a new window to display attendance
    view_window = tk.Toplevel(root)
    view_window.title("View Attendance")
    view_window.geometry("600x400")

    # Treeview widget to show the attendance data
    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Course", "Status", "Timestamp"), show="headings")

    # column heading
    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("Course", text="Course")
    tree.heading("Status", text="Status")
    tree.heading("Timestamp", text="Timestamp")

    # Set column width
    tree.column("ID", width=100)
    tree.column("Name", width=150)
    tree.column("Course", width=100)
    tree.column("Status", width=100)
    tree.column("Timestamp", width=100)

    # Fetch data from the database
    try:
        conn = sqlite3.connect("E:/8th sem/New folder/PythonProject/Database/attendance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, name, course, Status, timestamp FROM attendance")
        rows = cursor.fetchall()
        conn.close()

        # Insert data into the treeview
        for row in rows:
            tree.insert("", tk.END, values=row)

        tree.pack(expand=True, fill=tk.BOTH)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create the main window
root = tk.Tk()
root.title("Face Attendance System")
root.geometry("640x480")

# Background Image
bg_img = Image.open("Resources/app-bg.png")
bg_img = bg_img.resize((640, 480))
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Custom Styling
style = ttk.Style()
style.configure("TButton", borderwidth=5, font=("Arial", 14), padding=5, background="#00BFFF", foreground="black",
                activebackground="#5F9EA0", activeforeground="white")
style.configure("Title.TLabel", font=("Times", 20, "bold"), foreground="#333")


# Title Label
title_label = ttk.Label(root, text="Face Attendance System", style="Title.TLabel")
title_label.pack(pady=60)

# Buttons
take_attendance_btn = ttk.Button(root, text="Take Attendance", command=take_attendance)
take_attendance_btn.pack(pady=15, ipadx=20)

view_attendance_btn = ttk.Button(root, text="View Attendance", command=view_attendance)
view_attendance_btn.pack(pady=15, ipadx=20)

# Add Student Button
add_student_btn = ttk.Button(root, text="Add Student", command=lambda: open_add_student(root))
add_student_btn.pack(pady=15, ipadx=20)

remove_student_btn = ttk.Button(root, text="Remove Student", command=lambda: remove_student(root))
remove_student_btn.pack(pady=15, ipadx=20)

# Run the GUI
root.mainloop()
