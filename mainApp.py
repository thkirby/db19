import os
from datetime import datetime
import psycopg2
import psycopg2.extras
import random
from flask import Flask, request, render_template, g

# PostgreSQL IP address
IP_ADDR = "104.197.159.139"
# Create the application
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/see_rides", methods=['get', 'post'])
def see_rides():
    if "step" not in request.form:
        return render_template("see_rides.html", step="see_rides")

    elif request.form["step"] == "show_rides":
        db = get_db()
        cursor2 = db.cursor()

        # talk about adding another column to the car table so it isnt so... dumb
        cursor2.execute("select * from rides where custid=(%s)", [request.form['userID']])
        rowlist = cursor2.fetchall()
        print("after")
        return render_template("see_rides.html", step="show_rides", entries=rowlist)


@app.route("/schedule_ride", methods=['get', 'post'])
def schedule_ride():
    if "step" not in request.form:
        return render_template("schedule_ride.html", step="scheduled")

    elif request.form["step"] == "schedule_ride":
        db = get_db()
        cursor1 = db.cursor()
        cursor2 = db.cursor()
        cursor3 = db.cursor()
        cursor1.execute("select max(carid) from car")
        cursor2.execute("select max(resid) from reservation")
        resID = (cursor2.fetchone())[0]
        resID += 1
        upper = (cursor1.fetchone())[0]
        carid = random.randint(1, upper)

        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")

        print("before")
        # talk about adding another column to the car table so it isnt so... dumb
        cursor3.execute("insert into reservation (timeofres, place, resid, custid, carid) values (%s, %s, %s, %s, %s)", [request.form['pickupTime'], request.form['address'], resID, request.form['userID'], carid])
        print("after")
        db.commit()
        return render_template("add_car.html", added="add_car")


# This route is for adding a car to our database
# All it takes in is your longitude and latitude and assigns a Car ID
@app.route("/add_car", methods=['get', 'post'])
def add_car():
    if "added" not in request.form:
        return render_template("add_car.html", added="create_entry")

    elif request.form["added"] == "add_car":
        db = get_db()
        cursor1 = db.cursor()
        cursor2 = db.cursor()
        cursor1.execute("select max(carid) from car")
        custid1 = (cursor1.fetchone())[0]

        custid1 += 1
        print("before")
        # talk about adding another column to the car table so it isnt so... dumb
        cursor2.execute("insert into car (carid, caraddress, carmake, carmodel, carvin) values (%s, %s, %s, %s, %s)", [custid1, request.form['address'], request.form['make'], request.form['model'], request.form['carvin']])
        print("after")
        db.commit()
        return render_template("add_car.html", added="add_car")

@app.route("/delete_car", methods=['get','post'])
def delete_car():
    if "step" not in request.form:
        return render_template("delete_car.html", step="delete_entry")

    elif request.form['step'] == "delete_final":
        db = get_db()
        cursor1 = db.cursor()
        carid = int(request.form['carid'])
        carvin = request.form['carvin']

        cursor1.execute("delete from car where carid=%s", [carid])
        db.commit()
        return render_template("delete_car.html", step="delete_final")


@app.route("/user", methods=['get', 'post'])
def user_profile():

    if "step" not in request.form:
        return render_template("user_profile.html", step="compose_entry")

    elif request.form["step"] == "create_user":
        db = get_db()
        cursor1 = db.cursor()
        cursor2 = db.cursor()
        cursor1.execute("select max(custid) from customer")
        custid1 = (cursor1.fetchone())[0]

        custid1 += 1
        print("before")
        cursor2.execute("insert into customer (custid, firstname, lastname, accountinfo, phonenumber, email) values (%s, %s, %s, %s, %s, %s)", [custid1, request.form['firstName'], request.form['lastName'],request.form['creditCard'],request.form['phoneNumber'], request.form['email']])
        print("after")
        db.commit()
        return render_template("user_profile.html", step="create_user")

@app.route("/review", methods=['get', 'post'])
def review_a_ride():
    ID = int(request.form["ID"])
    value = int(request.form["value"])
    return render_template("review.html", ID = ID, value=value)


@app.route("/report", methods=['get', 'post'])
def report():
    if "incident_ID" not in request.form:
        return render_template("report.html", incidentID = "inc_report")

    elif request.form["incident_ID"] == "create_incID":
        db = get_db()
        cursor1 = db.cursor()
        cursor2 = db.cursor()
        cursor1.execute("select max(incidentid) from Incident")
        incidentID1 = (cursor1.fetchone())[0]

        incidentID1 += 1
        cursor2.execute("insert into incident (incidentid, carid, custid) values (%s, %s, %s)", [incidentID1, request.form['carid'], request.form['custid']])
        db.commit()
        return render_template("report.html", incident_ID="create_incID")


#####################################################
# Database handling


def connect_db():
    """Connects to the database."""
    debug("Connecting to DB.")
    conn = psycopg2.connect(host=IP_ADDR, user="postgres", password="rhodes", dbname="edisondb", 
        cursor_factory=psycopg2.extras.DictCursor)
    return conn


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'pg_db'):
        g.pg_db = connect_db()
    return g.pg_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database automatically when the application
    context ends."""
    debug("Disconnecting from DB.")
    if hasattr(g, 'pg_db'):
        g.pg_db.close()

######################################################
# Command line utilities 


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().execute(f.read())
    db.commit()


@app.cli.command('initdb')
def init_db_command():
    """Initializes the database."""
    print("Initializing DB.")
    init_db()

#####################################################
# Debugging


def debug(s):
    """Prints a message to the screen (not web browser) 
    if FLASK_DEBUG is set."""
    if app.config['DEBUG']:
        print(s)
