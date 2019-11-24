from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():

    return render_template("index.html")


@app.route("/user", methods=['get', 'post'])
def user_profile():

    if "creditCard" not in request.form:
        return render_template("user_profile.html")

    else:
        creditCard = int(request.form['creditCard'])
        phoneNumber = int(request.form['phoneNumber'])
        email = request.form(['email'])
        rideDrive = request.form(['rideDrive'])
        u = email+rideDrive
        return render_template("user_profile.html", userName=u,creditCard=creditCard, phoneNumber=phoneNumber, email=email, rideDrive=rideDrive)
