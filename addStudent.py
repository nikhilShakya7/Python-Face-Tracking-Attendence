import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

# Folder to store images
IMAGE_FOLDER = "Database/Images"

# Ensure the folder exists
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def open_add_student(root):
    def upload_photo():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            photo_label.config(text="Photo Selected")
            add_window.photo_path = file_path

    def save_student_to_db(student_id, name, course, photo_path):
        try:
            conn = sqlite3.connect("E:/8th sem/New folder/PythonProject/Database/attendance.db")
            cursor = conn.cursor()

            # Save image to the local folder
            ext = os.path.splitext(photo_path)[1]
            new_image_path = os.path.join(IMAGE_FOLDER, f"{student_id}{ext}")

            # Open and save the image in its original format
            img = Image.open(photo_path)
            img.save(new_image_path)

            # Read the image as binary (BLOB)
            with open(new_image_path, "rb") as file:
                image_blob = file.read()

            # Insert into database (Removed photo_path)
            cursor.execute('''
                INSERT INTO attendance (student_id, name, course, photo)
                VALUES (?, ?, ?, ?)
            ''', (student_id, name, course, image_blob))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully!")

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student ID already exists.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_details():
        student_id = id_entry.get()
        name = name_entry.get()
        course = course_entry.get()
        photo_path = getattr(add_window, "photo_path", None)

        if student_id and name and course and photo_path:
            save_student_to_db(student_id, name, course, photo_path)

            details_window = tk.Toplevel(add_window)
            details_window.title("Student Details")
            details_window.geometry("300x400")
            details_window.configure(bg="#f0f0f0")

            tk.Label(details_window, text=f"ID: {student_id}", font=("Arial", 14), bg="#f0f0f0", fg="#333").pack(pady=10)
            tk.Label(details_window, text=f"Name: {name}", font=("Arial", 14), bg="#f0f0f0", fg="#333").pack(pady=10)
            tk.Label(details_window, text=f"Course: {course}", font=("Arial", 14), bg="#f0f0f0", fg="#333").pack(pady=10)

            # Display the saved image
            img = Image.open(photo_path)
            img = img.resize((150, 150), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            img_label = tk.Label(details_window, image=img, bg="#f0f0f0")
            img_label.image = img
            img_label.pack(pady=10)

        else:
            messagebox.showerror("Error", "All fields are required!")

    add_window = tk.Toplevel(root)
    add_window.title("Add Student")
    add_window.geometry("400x500")
    add_window.configure(bg="#F5F5F5")

    title_label = tk.Label(add_window, text="Add Student", font=("Arial", 20, "bold"), bg="#F5F5F5", fg="#333")
    title_label.pack(pady=20)

    tk.Label(add_window, text="Student ID", font=("Arial", 12), bg="#F5F5F5", fg="#333").pack(pady=5)
    id_entry = tk.Entry(add_window, font=("Arial", 12), width=25, bd=2, relief="solid")
    id_entry.pack(pady=10)

    tk.Label(add_window, text="Name", font=("Arial", 12), bg="#F5F5F5", fg="#333").pack(pady=5)
    name_entry = tk.Entry(add_window, font=("Arial", 12), width=25, bd=2, relief="solid")
    name_entry.pack(pady=10)

    tk.Label(add_window, text="Course", font=("Arial", 12), bg="#F5F5F5", fg="#333").pack(pady=5)
    course_entry = tk.Entry(add_window, font=("Arial", 12), width=25, bd=2, relief="solid")
    course_entry.pack(pady=10)

    photo_label = tk.Label(add_window, text="No photo selected", font=("Arial", 12), bg="#F5F5F5", fg="#333")
    photo_label.pack(pady=10)

    upload_button = tk.Button(add_window, text="Upload Photo", font=("Arial", 12), bg="#4CAF50", fg="white",
                              relief="flat", width=20, height=2, command=upload_photo)
    upload_button.pack(pady=10)

    show_button = tk.Button(add_window, text="Show Detail & Add Student", font=("Arial", 12), bg="#007BFF", fg="white",
                            relief="flat", width=20, height=2, command=show_details)
    show_button.pack(pady=15)

    add_window.mainloop()
