import re, requests
from flask import request, render_template, redirect, session, url_for
from .models import db, User
from flask import current_app as app
from . import encpassword
from . import oauth


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    msg = ""
    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        userName = request.form["userName"]
        email = request.form["email"]
        password = request.form["password"]
        newPassword = encpassword.encrypt(password)

        if userName and email:
            existingUser = User.query.filter(User.userName == userName or User.email == email).first()
            if existingUser:
                msg = "Account already Exists"
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', userName):
                msg = 'Username must contain only characters and numbers!'
            else:
                newUser = User(
                    firstName=firstName,
                    lastName=lastName,
                    userName=userName,
                    email=email,
                    password=newPassword,
                )
                db.session.add(newUser)
                db.session.commit()
    return render_template("sign-up.html", msg=msg)


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if "loggedIn" in session:
        return redirect("/")
    if request.method == "POST":
        userName = request.form["userName"]
        password = request.form["password"]
        if userName and password:
            try:
                existingUser = User.query.filter(User.userName == userName).first()
                newPassword = encpassword.pwd_context.verify(password, existingUser.password)
                if existingUser and newPassword:
                    session["loggedIn"] = True
                    session["userName"] = userName
                    return redirect("/")
                else:
                    msg = "Username/Password incorrect"
            except AttributeError:
                msg = "Username/Password incorrect"
    return render_template("sign-in.html", msg=msg)


@app.route("/")
def home():
    if "loggedIn" in session or "user" in session:
        return render_template("index.html")

    return redirect("/login")


@app.route("/logout")
def logout():
    session.pop("loggedIn", None)
    session.pop("user", None)
    session.pop("userName", None)
    return redirect("/login")


@app.route("/callback")
def callback():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route("/auth")
def auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)

    print()
    session['user'] = user
    return redirect(url_for("home"))
