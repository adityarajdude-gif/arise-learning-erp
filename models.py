import sqlite3

DATABASE = "database.db"


def create_connection():
    return sqlite3.connect(DATABASE)


def create_tables():

    conn = create_connection()
    cursor = conn.cursor()

    # ==========================
    # ADMIN TABLE
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # ==========================
    # STUDENTS TABLE
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        father_name TEXT,
        mobile TEXT,
        course TEXT,
        address TEXT,
        fees INTEGER DEFAULT 0,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # ==========================
    # FEES TABLE
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        amount REAL,
        date TEXT,
        remarks TEXT,
        FOREIGN KEY(student_id)
        REFERENCES students(id)
    )
    """)

    # ==========================
    # ATTENDANCE TABLE
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT,
        FOREIGN KEY(student_id)
        REFERENCES students(id)
    )
    """)

    # ==========================
    # COURSES TABLE
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        duration TEXT,
        fees REAL
    )
    """)

    # ==========================
    # NOTICES TABLE
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Database Tables Created Successfully")


def insert_default_admin():

    conn = create_connection()
    cursor = conn.cursor()

    admin = cursor.execute(
        """
        SELECT * FROM admin
        WHERE username=?
        """,
        ("admin",)
    ).fetchone()

    if not admin:

        cursor.execute("""
        INSERT INTO admin
        (
            username,
            password
        )
        VALUES (?,?)
        """, (
            "admin",
            "admin123"
        ))

        conn.commit()

        print("Default Admin Created")

    conn.close()


def insert_sample_student():

    conn = create_connection()
    cursor = conn.cursor()

    student = cursor.execute(
        """
        SELECT * FROM students
        WHERE username=?
        """,
        ("st001",)
    ).fetchone()

    if not student:

        cursor.execute("""
        INSERT INTO students
        (
            name,
            father_name,
            mobile,
            course,
            address,
            fees,
            username,
            password
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?
        )
        """,
        (
            "Aditya Kumar",
            "Rajesh Kumar",
            "9876543210",
            "Python Full Stack",
            "Arrah, Bihar",
            15000,
            "st001",
            "123456"
        ))

        conn.commit()

        print("Sample Student Added")

    conn.close()


if __name__ == "__main__":

    create_tables()

    insert_default_admin()

    insert_sample_student()

    print("\nDatabase Ready Successfully")
    print("Admin Login")
    print("Username : admin")
    print("Password : admin123")

    print("\nStudent Login")
    print("Username : st001")
    print("Password : 123456")