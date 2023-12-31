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
    user = db.execute(f"SELECT cash FROM users WHERE id = {session['user_id']}")
    user_stocks = db.execute(f"SELECT shares, symbol, name FROM users_stocks JOIN stocks ON users_stocks.stock_id = stocks.id WHERE user_id = {session['user_id']}")
    total_stock = 0
    stock_data_list = []
    for stock in user_stocks:
        stock_data = (lookup(stock['symbol']))
        total_stock +=  stock_data['price'] * stock['shares']
        stock_data_list.append(stock_data)
    try:
        return render_template("portfolio.html", user=user[0], user_stocks=user_stocks, total_stock=total_stock, stock_data_list=stock_data_list)
    except:
        return apology("TODO")


def get_stock_id(symbol):
    return  db.execute(f"SELECT id FROM stocks WHERE symbol=\'{symbol}\';")

def is_empty(array):
    if len(array) == 0:
        return True
    else:
        return False


def insert_stocks(symbol, name):
    db.execute(f"INSERT INTO stocks(symbol, name) VALUES (\'{symbol}\', \'{name}\');")


def get_user_info(user_id, column):
    result = db.execute(f"SELECT {column} FROM users WHERE id = {user_id};")
    return result


def get_user_stock(user_id, stock_id):
    result = db.execute(f"SELECT shares FROM users_stocks JOIN stocks ON users_stocks.stock_id = stocks.id WHERE user_id = {user_id} AND stock_id = {stock_id};")                         
    return result;


def update_user_stock(user_id, stock_id, shares):
    db.execute(f"UPDATE users_stocks SET shares = {shares} WHERE user_id = {user_id} AND stock_id = {stock_id};")


def insert_user_stock(user_id, stock_id):
    db.execute(f"INSERT INTO users_stocks(user_id, stock_id) VALUES ({user_id},{stock_id})")


def deduct_user_cash(user_id, user_cash, stock_price):
    db.execute(f"UPDATE users SET cash = {user_cash - stock_price} WHERE id = {user_id};")


def add_user_cash(user_id, user_cash, stock_price):
    db.execute(f"UPDATE users SET cash = {user_cash + stock_price} WHERE id = {user_id};")


def record_transaction(user_id, stock_id, action, shares):
    if action == 'BUY' or action == 'SELL':
        db.execute(f"INSERT INTO history(user_id, action, stock_id, shares) VALUES ({user_id}, \'{action}\', {stock_id}, {shares});");
        return 0
    else:
        return 1

def delete_user_stock_entry(user_id, stock_id):
    db.execute(f"DELETE FROM users_stocks WHERE user_id = {user_id} AND stock_id = {stock_id};")


def get_history(user_id):
    return db.execute(f"SELECT action, shares, symbol, name FROM history JOIN stocks ON stocks.id = history.stock_id WHERE user_id = '{user_id}';")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history_db = get_history(session['user_id'])
    return render_template("history.html", history = history_db)


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
        stock_data = lookup(request.form['symbol'])
        if stock_data == None:
            error = "Stock not found"
            print(error)
            return apology(error)
        return render_template( "quote-info.html", stock=stock_data)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    elif request.method == "POST":
        pass
    stock_data = lookup(f"{request.form['symbol']}")
    if stock_data == None:
        error = "Stock not found"
        print(error) # DEBUG
        return apology(error)
    print(f"Stock data: {stock_data}") # DEBUG
    stock_db = get_stock_id(request.form['symbol'])
    if is_empty(stock_db):
        print(f"Stock not in database") # DEBUG
        insert_stocks(stock_data['name'], stock_data['symbol'])
        stock_db = get_stock_id(request.form['symbol'])
    print(f"StockID: {stock_db[0]['id']}") # DEBUG
    user = get_user_info(session['user_id'], "cash")
    print(f"User cash: {user[0]['cash']}") # DEBUG
    user_stocks = get_user_stock(session['user_id'], stock_db[0]['id'])
    print(f"User stocks: {user_stocks}") # DEBUG
    if stock_data['price'] > user[0]['cash']:
        error = "Not enough money"
        print(error)
        return apology(error)
    try:
        new_shares = user_stocks[0]['shares'] + 1
        update_user_stock(session['user_id'], stock_db[0]['id'], new_shares)
    except:
        print(f"User doesn't have any stock yet")
        new_shares = 1
        insert_user_stock(session['user_id'], stock_db[0]['id'])
    deduct_user_cash(session['user_id'],user[0]['cash'], stock_data['price'])
    record_transaction(session['user_id'], stock_db[0]['id'], 'BUY', new_shares)
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("sell.html")
    elif request.method == "POST":
        pass
    stock_data = lookup(f"{request.form['symbol']}")

    # DEBUG: in case API change and stock is not found
    if stock_data == None:
        error = "Stock not found"
        print(error)
        return apology(error)

    # Log
    print(f"Stock data: {stock_data}")

    # Setting variables for queries
    stock_db = get_stock_id(request.form['symbol'])
    user_stocks = get_user_stock(session['user_id'], stock_db[0]['id'])

    # DEBUG: in case user makes an error
    if is_empty(stock_db):
        error = "Stock not in database"
        print(error)
        apology(error)
    if len(user_stocks) == 0:
        error = "Doesn't own stock"
        print(error)
        return apology(error)

    # Log
    print(f"User stocks: {user_stocks}")

    new_shares = user_stocks[0]['shares'] - 1

    # Log
    print(f"New Shares: {new_shares}")

    user = get_user_info(session['user_id'], "cash")

    # Log
    print(f"User cash: {user[0]['cash']}")

    add_user_cash(session['user_id'],user[0]['cash'], stock_data['price'])
    if new_shares == 0:
        delete_user_stock_entry(session['user_id'], stock_db[0]['id'])
    else:
        update_user_stock(session['user_id'], stock_db[0]['id'], new_shares)
    record_transaction(session['user_id'], stock_db[0]['id'], 'SELL', new_shares)
    return redirect("/")
