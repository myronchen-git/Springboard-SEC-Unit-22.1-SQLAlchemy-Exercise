"""Blogly application."""

from flask import Flask, redirect, render_template, request
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

    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template("listusers.html", users=users)


@app.route("/users/new")
def display_add_user_form():
    """Displays the form to add a user."""

    return render_template("adduser.html")


@app.route("/users/new", methods=["post"])
def add_user():
    """Processes new user and redirect to list."""

    user = User(
        first_name=request.form["first-name"],
        last_name=request.form["last-name"],
        image_url=request.form["image-url"],
    )
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def user_details(user_id):
    """Show details about user."""

    user = User.query.get_or_404(user_id)

    return render_template("userdetails.html", user=user)


@app.route("/users/<int:user_id>/edit")
def display_edit_user_form(user_id):
    """Displays the form to edit a user."""

    user = User.query.get_or_404(user_id)

    return render_template("edituser.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["post"])
def edit_user(user_id):
    """Edits the user details."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["post"])
def delete_user(user_id):
    """Deletes a user."""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")
