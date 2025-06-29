# ===========================================================
# App Creation and Launch
# ===========================================================

from flask import (
    Flask,
    Response,
    render_template,
    redirect,
    flash,
    abort,
    request,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash
import html
import base64

from app.helpers.session import init_session
from app.helpers.db import connect_db
from app.helpers.errors import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.auth import login_required
from app.helpers.time import init_datetime, utc_timestamp, utc_timestamp_now


# Create the app
app = Flask(__name__)

# Configure app
init_session(app)  # Setup a session for messages, etc.
init_logging(app)  # Log requests
init_error(app)  # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps


# -----------------------------------------------------------
# Home page route
# -----------------------------------------------------------
@app.get("/")
def index():
    with connect_db() as client:
        # Select basic information about teams ordered by the team's player count.
        sql = """
            SELECT 
                teams.code, 
                teams.name, 
                COUNT(players.id) as player_count
            FROM teams
            LEFT JOIN players ON players.team = teams.code
            GROUP BY teams.code
            ORDER BY player_count DESC
        """
        result = client.execute(sql)

        return render_template("pages/home.jinja", teams=result.rows)


@app.get("/team-image/<code>")
def team_image(code):
    with connect_db() as client:
        sql = "SELECT image_data, image_mime FROM teams WHERE code = ?"
        result = client.execute(sql, [code])
        if not result.rows or not result.rows[0][0] or not result.rows[0][1]:
            abort(404)

        row = result.rows[0]
        return Response(row[0], mimetype=row[1])


# -----------------------------------------------------------
# About page route
# -----------------------------------------------------------
@app.get("/about/")
def about():
    return render_template("pages/about.jinja")


# -----------------------------------------------------------
# Things page route - Show all the things, and new thing form
# -----------------------------------------------------------
@app.get("/things/")
def show_all_things():
    with connect_db() as client:
        # Get all the things from the DB
        sql = """
            SELECT things.id,
                   things.name,
                   users.name AS owner

            FROM things
            JOIN users ON things.user_id = users.id

            ORDER BY things.name ASC
        """
        params = []
        result = client.execute(sql, params)
        things = result.rows

        # And show them on the page
        return render_template("pages/things.jinja", things=things)


# -----------------------------------------------------------
# Thing page route - Show details of a single thing
# -----------------------------------------------------------
@app.get("/thing/<int:id>")
def show_one_thing(id):
    with connect_db() as client:
        # Get the thing details from the DB, including the owner info
        sql = """
            SELECT things.id,
                   things.name,
                   things.price,
                   things.user_id,
                   users.name AS owner

            FROM things
            JOIN users ON things.user_id = users.id

            WHERE things.id=?
        """
        params = [id]
        result = client.execute(sql, params)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            thing = result.rows[0]
            return render_template("pages/thing.jinja", thing=thing)

        else:
            # No, so show error
            return not_found_error()


# -----------------------------------------------------------
# Route for adding a thing, using data posted from a form
# - Restricted to logged in users
# -----------------------------------------------------------
@app.post("/add")
@login_required
def add_a_thing():
    # Get the data from the form
    name = request.form.get("name")
    price = request.form.get("price")

    # Sanitise the text inputs
    name = html.escape(name)

    # Get the user id from the session
    user_id = session["user_id"]

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO things (name, price, user_id) VALUES (?, ?, ?)"
        params = [name, price, user_id]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Thing '{name}' added", "success")
        return redirect("/things")


# -----------------------------------------------------------
# Route for deleting a thing, Id given in the route
# - Restricted to logged in users
# -----------------------------------------------------------
@app.get("/delete/<int:id>")
@login_required
def delete_a_thing(id):
    # Get the user id from the session
    user_id = session["user_id"]

    with connect_db() as client:
        # Delete the thing from the DB only if we own it
        sql = "DELETE FROM things WHERE id=? AND user_id=?"
        params = [id, user_id]
        client.execute(sql, params)

        # Go back to the home page
        flash("Thing deleted", "success")
        return redirect("/things")


# -----------------------------------------------------------
# User registration form route
# -----------------------------------------------------------
@app.get("/register")
def register_form():
    return render_template("pages/register.jinja")


# -----------------------------------------------------------
# User login form route
# -----------------------------------------------------------
@app.get("/login")
def login_form():
    return render_template("pages/login.jinja")


# -----------------------------------------------------------
# Route for adding a user when registration form submitted
# -----------------------------------------------------------
@app.post("/add-user")
def add_user():
    # Get the data from the form
    username = request.form.get("username")
    password = request.form.get("password")

    # Sanitise the inputs)
    username = html.escape(username)

    # Hash the password
    hash = generate_password_hash(password)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)"
        values = [username, hash]
        result = client.execute(sql, values)

        if result.rows_affected == 0:
            flash("Username already exists.", "error")
            return redirect("/signup/")
        else:
            # Handle session
            session["userid"] = result.last_insert_rowid
            session["username"] = username

            flash(f"User {username} registered successfully", "success")
            return redirect("/")


# -----------------------------------------------------------
# Route for processing a user login
# -----------------------------------------------------------
@app.post("/login-user")
def login_user():
    # Get the login form data
    username = request.form.get("username")
    password = request.form.get("password")

    with connect_db() as client:
        # Attempt to find a record for that user
        sql = "SELECT * FROM users WHERE username = ?"
        values = [username]
        result = client.execute(sql, values)

        # Did we find a record?
        if result.rows:
            # Yes, so check password
            user = result.rows[0]
            hash = user[2]

            # Hash matches?
            if check_password_hash(hash, password):
                # Yes, so save info in the session
                session["userid"] = user[0]
                session["username"] = user[1]

                # And head back to the home page
                flash("Login successful", "success")
                return redirect("/")

        # Either username not found, or password was wrong
        flash("Invalid credentials", "error")
        return redirect("/login")


# -----------------------------------------------------------
# Route for processing a user logout
# -----------------------------------------------------------
@app.get("/logout")
def logout():
    # Clear the details from the session
    session.pop("userid", None)
    session.pop("username", None)

    # And head back to the home page
    flash("Logged out successfully", "success")
    return redirect("/")
