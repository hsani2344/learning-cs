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
    user = db.execute("SELECT cash FROM users")
    stock_id = db.execute(f"SELECT id FROM stocks WHERE symbol=\'{request.form['symbol']}\';");  
    user_stocks = db.execute(f"SELECT * FROM users_stocks JOIN stocks ON users_stocks.stock_id = stocks.id WHERE user_id = {session['user_id']} AND stock_id = {stock_id[0]['id']};")                         
    try:
        return render_template("portfolio.html", user=user[0], user_stocks=user_stocks)
    except:
        return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        stocks_data = lookup(f"{request.form['symbol']}")
        print(stocks_data)
        if stocks_data == None:
            return apology("Stock not found")
        try:
            db.execute(f"INSERT INTO stocks(symbol, name) VALUES (\'{stocks_data['name']}\', \'{stocks_data['symbol']}\');")
        except:
            pass
        stock_id = db.execute(f"SELECT id FROM stocks WHERE symbol=\'{request.form['symbol']}\';");
        user = db.execute(f"SELECT cash FROM users WHERE id = {session['user_id']};")
        user_stocks = db.execute(f"SELECT shares FROM users_stocks JOIN stocks ON users_stocks.stock_id = stocks.id WHERE user_id = {session['user_id']} AND stock_id = {stock_id[0]['id']};")                         
        if stocks_data['price'] > user[0]['cash']:
            return apology("Not enough money")
        try:
            new_shares = user_stocks[0]['shares'] + 1
            db.execute(f"UPDATE users_stocks SET shares = {new_shares} WHERE user_id = {session['user_id']} AND stock_id = {stock_id[0]['id']};")
        except:
            print(f"User doesn't have any stock yet")
            db.execute(f"INSERT INTO users_stocks(user_id, stock_id) VALUES ({session['user_id']},{stock_id[0]['id']})")
        db.execute(f"UPDATE users SET cash = {user[0]['cash'] - stocks_data['price']} WHERE id = {session['user_id']};")
        # return redirect("/")
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return render_template("history.html")


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
        db_username = db.execute(f"SELECT username FROM users WHERE username = \'{request.form['username']}\';")
        if len(db_username) > 0:
            error = 'Username taken'
            print(error)
            return apology(error)
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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # In case API change and stock is not found
    try:
        stocks_data = lookup(request.form['symbol'])
    except:
        error = "Stock not found"
        print(error)
        return apology(error)
    stocks = db.execute(f"SELECT shares FROM stocks WHERE symbol = \'{request.form['symbol']}\' AND user_id = {session['user_id']};")
    user = db.execute(f"SELECT cash FROM users WHERE id = {session['user_id']};")
    try:
        if stocks[0]['shares'] == 0:
            print("if")
            db.execute(f"DELETE FROM stocks WHERE symbol = \'{request.form['symbol']}\'AND user_id = {session['user_id']};")
        else:
            db.execute(f"UPDATE stocks SET shares = {stocks[0]['shares'] - 1} WHERE symbol = \'{request.form['symbol']}\' AND user_id = {session['user_id']};")
        db.execute(f" \
                   UPDATE users \
                      SET cash = {user[0]['cash'] + stocks_data['price']} \
                    WHERE id = {session['user_id']}; \
                   ")
    except:
        print(f"ERROR: You don\'t own any {request.form['symbol']}")
    return redirect("/")
