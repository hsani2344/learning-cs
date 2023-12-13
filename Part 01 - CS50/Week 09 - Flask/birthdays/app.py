import os

from sql import SQL
import sqlalchemy
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


# @app.after_request
# def after_request(response):
#     """Ensure responses aren't cached"""
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        name = request.form['name']
        birthday = request.form['birthday']
        id = db.execute(
            """
                SELECT id 
                  FROM birthdays
                 ORDER BY id DESC 
                 LIMIT 1;
            """
        )[0]['id'] + 1;
        db.execute(
            f"""
                INSERT INTO birthdays ( id, name, month, day )
                VALUES ({id}, '{name}', 12, 14);
            """
        )
        return "Success"
        # return redirect("/")

    else:
        # TODO: Display the entries in the database on index.html
        return render_template("index.html")


