import os

from sql import SQL
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

def home():
    birthday_list = db.execute(
        """
            SELECT *
              FROM birthdays
        """
    )
    return render_template("index.html", birthday_list = birthday_list)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form['name']
        day = int(request.form['birthday'][8:10])
        month = int(request.form['birthday'][5:7])
        try:
            id = int(db.execute(
                """
                    SELECT id 
                      FROM birthdays
                     ORDER BY id DESC 
                     LIMIT 1;
                """
            )[0]['id']) + 1
        except:
            id = 1
        db.execute(
            f"""
                INSERT INTO birthdays ( id, name, month, day )
                VALUES ({id}, '{name}', {month}, {day});
            """
        )
        return home()
    else:
        return home()
