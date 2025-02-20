# add_student.py
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def open_add_student(root):
    # Function to handle photo upload
    def upload_photo():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            photo_label.config(text="Photo Selected")
            add_window.photo_path = file_path

    # Function to show student details
    def show_details():
        student_id = id_entry.get()
        name = name_entry.get()
        photo_path = getattr(add_window, "photo_path", None)

        if student_id and name and photo_path:
            # Open a new window to show student details
            details_window = tk.Toplevel(add_window)
            details_window.title("Student Details")
            details_window.geometry("300x400")
            details_window.configure(bg="#f0f0f0")

            tk.Label(details_window, text=f"ID: {student_id}", font=("Arial", 14), bg="#f0f0f0", fg="#333").pack(pady=10)
            tk.Label(details_window, text=f"Name: {name}", font=("Arial", 14), bg="#f0f0f0", fg="#333").pack(pady=10)

            # Display the selected image
            img = Image.open(photo_path)
            img = img.resize((150, 150), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            img_label = tk.Label(details_window, image=img, bg="#f0f0f0")
            img_label.image = img
            img_label.pack(pady=10)

        else:
            messagebox.showerror("Error", "All fields are required!")

    # Create the "Add Student" window
    add_window = tk.Toplevel(root)
    add_window.title("Add Student")
    add_window.geometry("400x500")
    add_window.configure(bg="#F5F5F5")

    # Title Label
    title_label = tk.Label(add_window, text="Add Student", font=("Arial", 20, "bold"), bg="#F5F5F5", fg="#333")
    title_label.pack(pady=20)

    # Create the input fields for student details
    tk.Label(add_window, text="Student ID", font=("Arial", 12), bg="#F5F5F5", fg="#333").pack(pady=5)
    id_entry = tk.Entry(add_window, font=("Arial", 12), width=25, bd=2, relief="solid")
    id_entry.pack(pady=10)

    tk.Label(add_window, text="Name", font=("Arial", 12), bg="#F5F5F5", fg="#333").pack(pady=5)
    name_entry = tk.Entry(add_window, font=("Arial", 12), width=25, bd=2, relief="solid")
    name_entry.pack(pady=10)

    # Label to show if photo is selected
    photo_label = tk.Label(add_window, text="No photo selected", font=("Arial", 12), bg="#F5F5F5", fg="#333")
    photo_label.pack(pady=10)

    # Button to upload photo
    upload_button = tk.Button(add_window, text="Upload Photo", font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat", width=20, height=2, command=upload_photo)
    upload_button.pack(pady=10)

    # Button to show student details
    show_button = tk.Button(add_window, text="Show Details", font=("Arial", 12), bg="#007BFF", fg="white", relief="flat", width=20, height=2, command=show_details)
    show_button.pack(pady=15)
