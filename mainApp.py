import os
import psycopg2
import psycopg2.extras
from flask import Flask, request, render_template, g

# PostgreSQL IP address
IP_ADDR = "104.197.159.139"
# Create the application
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


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

