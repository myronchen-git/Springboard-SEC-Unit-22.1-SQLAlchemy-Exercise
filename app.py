"""Blogly application."""

from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import User, connect_db, db

# --------------------------------------------------

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
connect_db(app)
app.app_context().push()
db.create_all()

app.config["SECRET_KEY"] = "secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

# ==================================================


@app.route("/")
def root():
    return redirect("/users")


@app.route("/users")
def list_users():
    """Lists all users."""

    users = User.query.all()

    return render_template("listusers.html", users=users)
