import sqlite3

# Connect to SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect("E:/8th sem/New folder/PythonProject/Database/attendance.db")
cursor = conn.cursor()

# Create a table for storing student attendance (with a column for the photo path)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT UNIQUE,
        Name TEXT,
        Status TEXT DEFAULT 'Absent',
        Course TEXT,
        photo_path TEXT, 
        timestamp TEXT
    )
""")

# Save and close
conn.commit()
conn.close()

print("Database and table created successfully!")
