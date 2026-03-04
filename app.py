from flask import Flask, render_template, request, redirect, flash
import os
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = "jobtracker123"

# Function to get DB connection
def get_db():
    url = urlparse(os.environ.get("DATABASE_URL"))
    conn = psycopg2.connect(
        dbname=url.path[1:],  # skip the leading '/'
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return conn

# ----------------- Home / View Applications -----------------
@app.route("/")
def home():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM applications")
    apps = cur.fetchall()
    cur.close()
    db.close()
    return render_template("index.html",applications = apps)

# ----------------- Add Application -----------------
@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO applications (company,role,status) VALUES (%s,%s,%s)",(company,role,status))
        db.commit()
        cur.close()
        db.close()

        flash("Application added successfully","success")
        return redirect("/") # go back to home after submission
    return render_template("add.html")

# ----------------- Update Application -----------------
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM applications WHERE id=%s",(id,))
    app_data = cur.fetchone()

    if request.method == "POST":
        new_status = request.form["status"]
        cur.execute("UPDATE applications SET status = %s WHERE id=%s",(new_status,id))
        db.commit()
        cur.close()
        db.close()

        flash("Application updated successfully ✅","success")  # ⭐ added
        return redirect("/")
    cur.close()
    db.close()
    return render_template("update.html", app=app_data)

# ----------------- Delete Application -----------------
@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    cur = db.cursor()
    
    cur.execute("DELETE FROM applications WHERE id= %s", (id,))
    db.commit()

    cur.close()
    db.close()

    flash("Application deleted","danger")
    return redirect("/")

# ----------------- Run App -----------------
if __name__ == "__main__":
    app.run()