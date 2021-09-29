from app import app 
from db import db
from flask import render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint, shuffle
from forms import RegisterForm, LoginForm
import sql_commands

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    return render_template("start.html")

@app.route("/quiz")
def quiz():
    total = sql_commands.question_count()

    question_ids = set()
    while len(question_ids) < 10:
        question_ids.add(randint(1, total))

    questions = {}    
    for question_id in question_ids:
        options = sql_commands.get_options(question_id)
        shuffle(options)
        questions[question_id] = options

    return render_template("quiz.html", questions=questions)

@app.route("/result", methods=["POST"])
def result():
    results = request.form
    score = 0

    for key in results.keys():
        value = results.get(key)
        correct = sql_commands.is_correct(value)
        if correct:
            score += 1
        if "user_id" in session:
            sql_commands.add_answer(value, session["user_id"])

    return render_template("finish.html", score=score)


@app.route("/scoreboard")
def scoreboard():
    scoreboard = sql_commands.get_scoreboard()   
    return render_template("scoreboard.html", scoreboard=scoreboard)

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/")

    if request.method == "GET":
        form = LoginForm()
    else:
        form = LoginForm(request.form)
        if form.validate_on_submit():      
            user = sql_commands.get_user(form.username.data)
            if not user:
                flash("Käyttäjätunnus tai salasana olivat vääriä", "danger")
                return redirect("/login")
            else:
                hash_value = user.password
                if check_password_hash(hash_value, form.password.data):
                    session["user_id"] = user.id
                    flash(f"Kirjauduttu sisään käyttäjänä {form.username.data}", "success")
                    return redirect("/")
                else:
                    flash("Käyttäjätunnus tai salasana olivat vääriä", "danger")
                    return redirect("/login")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect("/")

    if request.method == "GET":
        form = RegisterForm()
    else:
        form = RegisterForm(request.form)
        if form.validate_on_submit():      
            user = sql_commands.get_user(form.username.data)
    
            if user:
                flash("Käyttäjänimi on jo käytössä", "danger")
                return render_template("register.html", form=form)
    
            hash_value = generate_password_hash(form.password.data)
            sql_commands.add_user(form.username.data, hash_value)
            flash(f"Käyttäjätunnus luotu käyttäjälle {form.username.data}", "success")
    
            return redirect("/")

    return render_template("register.html", form=form)
        
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/")

    scores = sql_commands.get_user_scores(session["user_id"])
    return render_template("profile.html", scores=scores)