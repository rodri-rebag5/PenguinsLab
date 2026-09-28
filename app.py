
import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from additional_functions import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#Connect DB to Python program
connection = sqlite3.connect("penguinslab.db", check_same_thread=False)
db = connection.cursor()


#Home Page
@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")

#Profile
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    user_data = db.execute("SELECT * FROM users WHERE email = ?", [session["user_id"]]).fetchall()

    return render_template("profile.html", user_name = user_data[0][1], user_lastname = user_data[0][2], country = user_data[0][3], email = user_data[0][7], birth_day = user_data[0][4], birth_month = user_data[0][5], birth_year = user_data[0][6])

#Login
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return redirect("/login")

        # Query database for username
        rows = (db.execute("SELECT * FROM users WHERE email = ?", [request.form.get("username")])).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][8], request.form.get("password")):
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0][7]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#Register
@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

        # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure name was submitted
        if not request.form.get("name"):
            flash("Please provide your name")
            return redirect("/register")
        
        # Ensure last name was submitted
        elif not request.form.get("last_name"):
            flash("Please provide your last name")
            return redirect("/register")

        # Ensure email was submitted
        elif not request.form.get("username"):
            flash("Please provide your e-mail")
            return redirect("/register")

        # Ensure country was submitted
        elif not request.form.get("country"):
            flash("Please provide your country")
            return redirect("/register")

        # Ensure birth day was submitted
        elif not request.form.get("birth_day"):
            flash("Please provide your birth day")
            return redirect("/register")
        # Ensure birth month was submitted
        elif not request.form.get("birth_month"):
            flash("Please provide your birth month")
            return redirect("/register")
        # Ensure birth year was submitted
        elif not request.form.get("birth_year"):
            flash("Please provide your birth year")
            return redirect("/register")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please enter a password")
            return redirect("/register")

        #Ensure password was confirmed
        elif not request.form.get("confirmation"):
            flash("Please confirm your password")
            return redirect("/register")

        #Ensure password and confirmation match
        elif request.form.get("confirmation") != request.form.get("password"):
            flash("Passwords do not match")
            return redirect("/register")

        #Make sure username doesn't exist
        rows = (db.execute("SELECT * FROM users WHERE email = ?", [request.form.get("username")])).fetchall()
        
        if len(rows) != 0:
            flash("Email already registered")
            return redirect("/register")

        #Insert new user into database
        db.execute("INSERT INTO users (user_name, user_lastname, country, birth_day, birth_month, birth_year, email, passwrd) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (request.form.get("name"), request.form.get("last_name"), request.form.get("country"), request.form.get("birth_day"), request.form.get("birth_month"), request.form.get("birth_year"), request.form.get("username"), generate_password_hash(request.form.get("password"))))  
        connection.commit()

        # Query database for new user
        rows = (db.execute("SELECT * FROM users WHERE email = ?", [request.form.get("username")])).fetchall()

        # Remember which user has logged in
        session["user_id"] = rows[0][7]

        # Redirect user to home page
        flash("Succesfully registered")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


#My Courses
@app.route("/mycourses", methods=["GET", "POST"])
@login_required
def mycourses():

    if request.method == "POST":

        selected_course_name = request.form.get("select_course")

        selected_course_info = db.execute("SELECT * FROM courses WHERE course_name = ?", [selected_course_name]).fetchall()
        enrolled = db.execute("SELECT enrolled FROM user_courses WHERE course_name = ? AND email = ?", ([selected_course_name, session["user_id"]])).fetchall() 

        if len(enrolled) != 1:
            enrolled = [(0)]
        
        return render_template("selected_course.html", selected_course_info = selected_course_info, enrolled = enrolled)


    else:

        courses_list = db.execute("SELECT * FROM user_courses WHERE email = ?", [session["user_id"]]).fetchall()

        return render_template("mycourses.html", courses_list = courses_list)




#All Courses
@app.route("/courses", methods=["GET", "POST"])
def courses():

    if request.method == "POST":

        selected_course_name = request.form.get("select_course")

        selected_course_info = db.execute("SELECT * FROM courses WHERE course_name = ?", [selected_course_name]).fetchall()

        enrolled = db.execute("SELECT enrolled FROM user_courses WHERE course_name = ? AND email = ?", ([selected_course_name, session["user_id"]])).fetchall() 

        if len(enrolled) != 1:
            enrolled = [(0)]
        
        return render_template("selected_course.html", selected_course_info = selected_course_info, enrolled = enrolled)

    else: 

        courses_list = db.execute("SELECT * FROM courses").fetchall()
    
        return render_template("courses.html", courses_list = courses_list)
    


#Selected Course
@app.route("/selected_course", methods=["GET", "POST"])
def selected_course():

    if request.method == "POST":

        #Check if user is already enrolled

        course_id = request.form.get("select_course_id")

        check = db.execute("SELECT * FROM user_courses WHERE course_id = ? AND email = ?", ([course_id, session["user_id"]])).fetchall()

        if len(check) != 0:
            courses_list = db.execute("SELECT * FROM user_courses WHERE email = ?", [session["user_id"]]).fetchall()
            return render_template("/mycourses.html", courses_list = courses_list)
        
        #Enroll user to class
        
        user_number_courses = db.execute("SELECT ncourses FROM users WHERE email = ?", [session["user_id"]]).fetchall()
        course_participants = db.execute("SELECT participants FROM courses WHERE course_id = ?", [course_id]).fetchall()
        course_name = db.execute("SELECT course_name FROM courses WHERE course_id = ?", [course_id]).fetchall()

        user_number_courses = user_number_courses[0][0] + 1
        course_participants = course_participants[0][0] + 1

        db.execute("UPDATE users SET ncourses = ? WHERE email = ?", (user_number_courses, session["user_id"]))
        db.execute("UPDATE courses SET participants = ? WHERE course_id = ?", (course_participants, course_id))
        db.execute("INSERT INTO user_courses (course_id, course_name, email, enrolled) VALUES (?, ?, ?, ?)", (course_id, course_name[0][0], session["user_id"], 1))
        connection.commit()

        courses_list = db.execute("SELECT * FROM user_courses WHERE email = ?", [session["user_id"]]).fetchall()

        return render_template("/mycourses.html", courses_list = courses_list)

    
    else:
        
        return render_template("selected_course.html")

#Logout
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
