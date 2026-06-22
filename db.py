import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Admin Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Students Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    father_name TEXT,
    mobile TEXT,
    course TEXT,
    address TEXT,
    fees INTEGER,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Fees Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS fees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    amount INTEGER,
    date TEXT,
    remarks TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

# Attendance Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

# Insert Default Admin
cursor.execute("""
INSERT INTO admin(username,password)
VALUES('admin','admin123')
""")

conn.commit()
conn.close()

print("Database Created Successfully!")