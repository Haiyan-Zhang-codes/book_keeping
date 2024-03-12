import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from cs50 import SQL

db = SQL("sqlite:///data/app.db")

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not name or not password or password != confirmation:
           return apology("Field cannot be empty or password is not identical")
        else:
            hashedPassword = generate_password_hash(password)
            try:
                db.execute("INSERT INTO users (username, hash) VALUES(?,?)", name, hashedPassword)
                return render_template("login.html")
            except (ValueError):
                return apology("username exists")
            
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/book_keeping", methods=["GET","POST"])
def book_keeping():
    if request.method == "GET":
        categories = ["Salary","Pension","Grocery","Tuition fees","Phone bill","Car","Home"]
        types = ["Income", "Expense"]
        return render_template("book_keeping.html",categories = categories, types = types)
    elif request.method == "POST":
        amount = request.form.get("amount")
        category = request.form.get("category")
        transaction_type = request.form.get("type")
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        user_id = session.get("user_id")
        db.execute("INSERT INTO book_keeping (user_id, amount, category, type, year, month, date) VALUES(?,?,?,?,?,?,?)",user_id,amount,category,transaction_type,year,month,day)
        return redirect("/report")

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "GET":
        years = range(2000, datetime.now().year+1)
        return render_template("report.html",years = years)
    elif request.method == "POST":
        user_id = session.get("user_id")
        action = request.form.get("action")
        if action == "yearly":
            year = request.form.get("year")
            yearly_data_category = db.execute("SELECT SUM(amount) AS total_amount, category, type, year FROM book_keeping WHERE year = ? AND user_id = ? GROUP BY category", year,user_id)
            yearly_data_type = db.execute("SELECT SUM(amount) AS total_amount,type, year FROM book_keeping WHERE year = ? AND user_id = ? GROUP BY type", year,user_id)
            print(yearly_data_category)
            print(yearly_data_type)
            income_count = sum(1 for item in yearly_data_category if item['type'] == "Income")
            expense_count = sum(1 for item in yearly_data_category if item['type'] == "Expense")
            total_income = sum(item['total_amount'] for item in yearly_data_type if item['type']=="Income")
            total_expense = sum(item['total_amount'] for item in yearly_data_type if item['type']=="Expense")
            balance = total_income-total_expense
            return render_template("report.html", yearly_data_category=yearly_data_category,yearly_data_type=yearly_data_type,action=action,income_count=income_count,expense_count=expense_count,balance=balance)
        
        elif action == "monthly":
            month_year_str = request.form.get("month")
            year, month = month_year_str.split('-')
            year = int(year)
            month = int(month)
            monthly_data_category = db.execute("SELECT SUM(amount) AS total_amount, category, type, year FROM book_keeping WHERE year = ? AND month = ? AND user_id = ? GROUP BY category", year, month,user_id)
            monthly_data_type = db.execute("SELECT SUM(amount) AS total_amount, type, year FROM book_keeping WHERE year = ? AND month = ? AND user_id = ? GROUP BY type", year, month, user_id)
            print(monthly_data_category)
            print(monthly_data_type)
            return render_template("report.html", monthly_data_category=monthly_data_category, monthly_data_type=monthly_data_type,action=action)
    else:
        return render_template("apoogy.html")

# @app.route("/report/yearly_report")
# def yearly_report():
#     return render_template("yearly_report.html")

# @app.route("/report/monthly_report")
# def yearly_report():
#     return render_template("monthly_report.html")




@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")