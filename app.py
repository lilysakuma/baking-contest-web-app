"""
Name: Lily Sakuma
Date: 11/10/2026
Assignment: 5
Due Date: 11/20/2026
About this project: This project creates a basic baking contest website using Python, Flask, and SQLite3. 
Users can register for the baking contest, submit baking entries with vote counts, and view the lists of 
registered users and contest results. The program also checks user input and displays error messages when 
information is invalid.
Assumptions: A user must already be registered before submitting a baking contest entry.
Usernames are entered exactly as they appear in the database.
If multiple users have the same name, the program uses the first matching user.
The database is initialized before running the website.
The website is run in an environment with Python 3 and Flask installed.
All work below was performed solely by Lily Sakuma.
I used AI-generated code and AI assistance to help develop, understand, and debug this assignment.
"""
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

# Since this project was made for a class, passwords are stored
# as plain text to keep things simple. If this were a real-world
# application, I would hash the passwords before storing them
# and make sure they were never displayed to other users.
# This project is intended for demonstration purposes only.
@app.route("/add_user", methods=["GET", "POST"])
def add_user():

    if request.method == "GET":
        return render_template("add_user.html")

    # Get the information entered in the form
    name = request.form.get("name", "").strip()
    age = request.form.get("age", "").strip()
    phone = request.form.get("phone", "").strip()
    security = request.form.get("security", "").strip()
    password = request.form.get("password", "")

    errors = []

    # Check each input
    if not name:
        errors.append("Name cannot be empty.")

    if not age.isdigit() or not 1 <= int(age) <= 120:
        errors.append("Age must be between 1 and 120.")

    if not phone:
        errors.append("Phone number cannot be empty.")

    if not security.isdigit() or int(security) not in (1, 2, 3):
        errors.append("Security level must be 1, 2, or 3.")

    if not password.strip():
        errors.append("Password cannot be empty.")

    # Display all errors if any inputs are invalid
    if errors:
        return render_template("result.html", msg="\n".join(errors))

    # Add the contestant to the database
    conn = sqlite3.connect("contest.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO BakingContestPeople
        (Name, Age, PhoneNumber, SecurityLevel, LoginPassword)
        VALUES (?, ?, ?, ?, ?)
    """, (name, int(age), phone, int(security), password))

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        msg="New baking contest user added successfully!"
    )
#Display all registered baking contest users
@app.route("/list_users")
def list_users():
    
    #Connect to the database
    conn = sqlite3.connect("contest.db")
    cursor = conn.cursor()
    
    #Get all users from the database
    cursor.execute("""
        SELECT Name, Age, PhoneNumber, SecurityLevel, LoginPassword
        FROM BakingContestPeople
    """)
    
    users = cursor.fetchall()
    
    conn.close()
    
    return render_template("list_users.html", users=users)

@app.route("/list_results")
def list_results():
    #Connect to the database
    conn = sqlite3.connect("contest.db")
    cursor = conn.cursor()
    
    #Get all baking contest entries
    cursor.execute("""
        SELECT EntryID, UserID, NameOfBakingItem,
                NumExcellentVotes, NumOkVotes, NumBadVotes
        FROM BakingContestEntry
    """)
    
    entries = cursor.fetchall()
    
    conn.close()
    
    return render_template("list_results.html", entries=entries)


# Add a new baking contest entry
@app.route("/add_entry", methods=["GET", "POST"])
def add_entry():

    # Show the form when the user first visits the page
    if request.method == "GET":
        return render_template("add_entry.html")

    # Get the information submitted from the form
    username = request.form.get("username", "").strip()
    item = request.form.get("item", "").strip()
    excellent = request.form.get("excellent", "").strip()
    ok = request.form.get("ok", "").strip()
    bad = request.form.get("bad", "").strip()

    errors = []

    # Check the name and baking item
    if not username:
        errors.append("Name of user cannot be empty.")

    if not item:
        errors.append("Name of baking item cannot be empty.")

    # Make sure all vote counts are nonnegative integers
    if not excellent.isascii() or not excellent.isdecimal():
        errors.append("Excellent votes must be a nonnegative integer.")

    if not ok.isascii() or not ok.isdecimal():
        errors.append("OK votes must be a nonnegative integer.")

    if not bad.isascii() or not bad.isdecimal():
        errors.append("Bad votes must be a nonnegative integer.")

    # Connect to the database
    conn = sqlite3.connect("contest.db")
    cursor = conn.cursor()

    # Look for the contestant by name
    user = None

    if username:
        cursor.execute(
            "SELECT UserId FROM BakingContestPeople WHERE Name = ?",
            (username,)
        )

        user = cursor.fetchone()

        if user is None:
            errors.append("The user does not exist in the database.")

    # Show all errors if anything is invalid
    if errors:
        conn.close()
        return render_template("result.html", msg="\n".join(errors))

    # Add the baking entry to the database
    cursor.execute("""
        INSERT INTO BakingContestEntry
        (UserId, NameOfBakingItem, NumExcellentVotes,
         NumOkVotes, NumBadVotes)
        VALUES (?, ?, ?, ?, ?)
    """, (user[0], item, int(excellent), int(ok), int(bad)))

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        msg="New baking contest entry added successfully!"
    )

if __name__ == "__main__":
    app.run(port=50001, debug=False)
