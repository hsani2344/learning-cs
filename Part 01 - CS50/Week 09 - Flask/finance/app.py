import os

from sql import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Create an array of dict with
    # Stock price and symbol
    # Number of shares from database
    # Money
    # try:
        # return render_template("portfolio.html", stock=stock, portfolio=portfolio)
    # except:
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        stocks_data = lookup(f"{request.form['symbol']}")
        if stocks_data == None:
            return apology("Stock not found")
        user = db.execute(f"SELECT cash FROM users WHERE id = {session['user_id']};")
        user_stocks = db.execute(f"SELECT * FROM stocks WHERE id = {session['user_id']} AND symbol = \'{request.form['symbol']}\';")                         
        if stocks_data['price'] > user[0]['cash']:
            return apology("Not enough money")
        # try:
        #     # Condition
        #     # Increase if .count is not empty
        #     # Else insert into table
        #     portfolio = db.execute(
        #         f"""
        #             SELECT * FROM "{request.form['symbol']}" WHERE user_id = {session['user_id']};
        #         """
        #     )
        # except:
        #     print(f"ERROR: TABLE \"{request.form['symbol']}\" does not exist")
        #     db.execute(
        #         f"""
        #             CREATE TABLE "{request.form['symbol']}" (
        #                 id SERIAL AUTO_INCREMENT UNIQUE,
        #                 user_id SERIAL UNIQUE NOT NULL,
        #                 shares INT UNSIGNED NOT NULL DEFAULT 1,
        #                 PRIMARY KEY (id)
        #                 FOREIGN KEY (user_id) REFERENCES users(id)
        #             );
        #         """
        #     )
        #     db.execute(
        #         f"""
        #             UPDATE "users"
        #             SET cash = {user[0].cash - stock.price}
        #             WHERE user_id = {session['user_id']};
        #         """
        #     )
        # try:
        #     db.execute(
        #         f"""
        #             UPDATE "{request.form['symbol']}"
        #             SET shares = {portfolio[0]['shares'] + 1}
        #             WHERE user_id = {session['user_id']};
        #         """
        #     )
        #     print(user[0]['cash'] - stock['price'])
        #     db.execute(
        #         f"""
        #             UPDATE "users"
        #             SET cash = {user[0]['cash'] - stock['price']}
        #             WHERE id = {session['user_id']};
        #         """
        #     )
        # except:
        #     print(f"ERROR: User #{session['user_id']} does not exist in TABLE \"{request.form['symbol']}\"")
        #     db.execute(
        #         f"""
        #             INSERT INTO "{request.form['symbol']}"(user_id)
        #             VALUES ({session['user_id']});
        #         """
        #     )
        #     db.execute(
        #         f"""
        #             UPDATE "users"
        #             SET cash = {user[0].cash - stock.price}
        #             WHERE user_id = {session['user_id']};
        #         """
        #     )
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        return render_template(
                               "layout.html",
                               # Get stock symbol, name and price
                               stock=lookup(request.form['symbol'])
                               )


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        if request.form['username'] == '' or request.form['password'] == '':
            error = 'Form unfilled'
            print(error)
            return apology(error)
        try:
            db.execute(
                       f"""
                           INSERT INTO users(username, hash)
                           VALUES (\'{request.form['username']}\', \'{generate_password_hash(request.form['password'])}\');
                       """)
            session["user_id"] = db.execute(
                               f"""
                               SELECT id
                                 FROM users
                                WHERE username = \'{request.form['username']}\';
                               """)[0]['id']
            return redirect("/")
        except:
            error = 'Username taken'
            return apology(error)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # TODO Sell
    # TODO Record the action in a history
    # TODO ERROR #1: I don't have any stock
    # TODO ERROR #2: Stock does not exist
    return apology("TODO")
