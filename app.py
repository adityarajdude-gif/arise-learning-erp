from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "arise_learning_secret"

DATABASE = "database.db"


# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return render_template("login.html")


# -------------------------
# LOGIN
# -------------------------
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    conn = get_db()
    cur = conn.cursor()

    if role == "admin":

        admin = cur.execute(
            """
            SELECT * FROM admin
            WHERE username=? AND password=?
            """,
            (username, password)
        ).fetchone()

        if admin:
            session["admin"] = admin["username"]
            return redirect("/admin/dashboard")

    elif role == "student":

        student = cur.execute(
            """
            SELECT * FROM students
            WHERE username=? AND password=?
            """,
            (username, password)
        ).fetchone()

        if student:
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]
            return redirect("/student/dashboard")

    flash("Invalid Login")
    return redirect("/")


# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================
# ADMIN SECTION
# =========================

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/")

    conn = get_db()

    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_fees = conn.execute(
        "SELECT IFNULL(SUM(amount),0) FROM fees"
    ).fetchone()[0]

    return render_template(
        "admin/dashboard.html",
        total_students=total_students,
        total_fees=total_fees
    )


# -------------------------
# STUDENTS LIST
# -------------------------
@app.route("/admin/students")
def students():

    if "admin" not in session:
        return redirect("/")

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    return render_template(
        "admin/students.html",
        students=students
    )


# -------------------------
# ADD STUDENT
# -------------------------
@app.route("/admin/add-student", methods=["GET", "POST"])
def add_student():

    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":

        name = request.form["name"]
        father_name = request.form["father_name"]
        mobile = request.form["mobile"]
        course = request.form["course"]
        address = request.form["address"]
        fees = request.form["fees"]
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        conn.execute(
            """
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
            VALUES (?,?,?,?,?,?,?,?)
            """,
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
        )

        conn.commit()

        flash("Student Added Successfully")

        return redirect("/admin/students")

    return render_template("admin/add_student.html")


# -------------------------
# EDIT STUDENT
# -------------------------
@app.route("/admin/edit-student/<int:id>",
           methods=["GET", "POST"])
def edit_student(id):

    if "admin" not in session:
        return redirect("/")

    conn = get_db()

    if request.method == "POST":

        conn.execute(
            """
            UPDATE students
            SET
            name=?,
            father_name=?,
            mobile=?,
            course=?,
            address=?,
            fees=?
            WHERE id=?
            """,
            (
                request.form["name"],
                request.form["father_name"],
                request.form["mobile"],
                request.form["course"],
                request.form["address"],
                request.form["fees"],
                id
            )
        )

        conn.commit()

        flash("Student Updated")
        return redirect("/admin/students")

    student = conn.execute(
        """
        SELECT * FROM students
        WHERE id=?
        """,
        (id,)
    ).fetchone()

    return render_template(
        "admin/edit_student.html",
        student=student
    )


# -------------------------
# DELETE STUDENT
# -------------------------
@app.route("/admin/delete-student/<int:id>")
def delete_student(id):

    if "admin" not in session:
        return redirect("/")

    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()

    flash("Student Deleted")

    return redirect("/admin/students")


# -------------------------
# FEES MANAGEMENT
# -------------------------
@app.route("/admin/fees", methods=["GET", "POST"])
def fees():

    if "admin" not in session:
        return redirect("/")

    conn = get_db()

    if request.method == "POST":

        student_id = request.form["student_id"]
        amount = request.form["amount"]

        conn.execute(
            """
            INSERT INTO fees
            (
                student_id,
                amount,
                date,
                remarks
            )
            VALUES (?,?,?,?)
            """,
            (
                student_id,
                amount,
                datetime.now().strftime("%Y-%m-%d"),
                "Fee Deposit"
            )
        )

        conn.commit()

        flash("Fee Added")

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    fee_records = conn.execute(
        """
        SELECT fees.*,
        students.name
        FROM fees
        JOIN students
        ON fees.student_id=students.id
        ORDER BY fees.id DESC
        """
    ).fetchall()

    return render_template(
        "admin/fees.html",
        students=students,
        fee_records=fee_records
    )


# =========================
# STUDENT SECTION
# =========================

@app.route("/student/dashboard")
def student_dashboard():

    if "student_id" not in session:
        return redirect("/")

    conn = get_db()

    student = conn.execute(
        """
        SELECT * FROM students
        WHERE id=?
        """,
        (session["student_id"],)
    ).fetchone()

    return render_template(
        "student/dashboard.html",
        student=student
    )


# -------------------------
# PROFILE
# -------------------------
@app.route("/student/profile")
def profile():

    if "student_id" not in session:
        return redirect("/")

    conn = get_db()

    student = conn.execute(
        """
        SELECT * FROM students
        WHERE id=?
        """,
        (session["student_id"],)
    ).fetchone()

    return render_template(
        "student/profile.html",
        student=student
    )


# -------------------------
# STUDENT FEES
# -------------------------
@app.route("/student/fees")
def student_fees():

    if "student_id" not in session:
        return redirect("/")

    conn = get_db()

    records = conn.execute(
        """
        SELECT *
        FROM fees
        WHERE student_id=?
        ORDER BY id DESC
        """,
        (session["student_id"],)
    ).fetchall()

    return render_template(
        "student/fees.html",
        records=records
    )


# -------------------------
# ATTENDANCE
# -------------------------
@app.route("/student/attendance")
def attendance():

    if "student_id" not in session:
        return redirect("/")

    conn = get_db()

    attendance = conn.execute(
        """
        SELECT *
        FROM attendance
        WHERE student_id=?
        ORDER BY date DESC
        """,
        (session["student_id"],)
    ).fetchall()

    return render_template(
        "student/attendance.html",
        attendance=attendance
    )


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)