from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# Database setup
def init_db():
    conn = sqlite3.connect("employees.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    salary REAL NOT NULL,
                    designation TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()


init_db()


# Routes
@app.route("/")
def index():
    conn = sqlite3.connect("employees.db")
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    employees = c.fetchall()
    conn.close()
    return render_template("index.html", employees=employees)


@app.route("/add", methods=["POST"])
def add_employee():
    emp_id = request.form["emp_id"]
    name = request.form["name"]
    salary = request.form["salary"]
    designation = request.form["designation"]

    conn = sqlite3.connect("employees.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO employees (id, name, salary, designation) VALUES (?, ?, ?, ?)",
                  (emp_id, name, salary, designation))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # ignore duplicate IDs
    conn.close()
    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update_role():
    emp_id = request.form["emp_id"]
    new_role = request.form["designation"]

    conn = sqlite3.connect("employees.db")
    c = conn.cursor()
    c.execute("UPDATE employees SET designation=? WHERE id=?", (new_role, emp_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

