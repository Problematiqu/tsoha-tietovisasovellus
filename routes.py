from app import app 
from db import db
from flask import render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint, shuffle

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    return render_template("start.html")

@app.route("/quiz")
def quiz():
    sql = "SELECT COUNT(id) FROM questions"
    result = db.session.execute(sql)
    total = result.fetchone()[0]

    question_numbers = set()
    while len(question_numbers) < 10:
        question_numbers.add(randint(1, total))

    questions = {}    
    for number in question_numbers:
        sql = "SELECT q.question, o.option, o.correct, o.id FROM questions q LEFT JOIN options o ON q.id = o.question_id WHERE q.id=:number"
        result = db.session.execute(sql, {"number": number}) 
        answers = result.fetchall()
        shuffle(answers)
        questions[number] = answers

    return render_template("quiz.html", questions=questions)

@app.route("/result", methods=["POST"])
def result():
    results = request.form
    correct_answers = 0
    for key in results.keys():
        value = results.get(key)
        sql = "SELECT correct FROM options WHERE id=:value"
        query_result = db.session.execute(sql, {"value": value})
        correct = query_result.fetchone()[0]
        if correct:
            correct_answers += 1

    return render_template("finish.html", score=correct_answers)


@app.route("/scoreboard")
def scoreboard():
    return render_template("scoreboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT username, password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username": username})
        user = result.fetchone()
        if not user:
            flash("Tunnus tai salasana olivat väärin")
            return redirect("/login")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = user.username
                return redirect("/")
            else:
                flash("Käyttäjätunnus tai salasana olivat vääriä")
                return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        repeated_password = request.form["repeated_password"]

        if password != repeated_password:
            flash("Salasanat eivät olleet samoja")
            return redirect("/register")
        
        sql = "SELECT username FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username": username})
        user = result.fetchone()

        if user:
            flash("Käyttäjänimi on jo käytössä")
            return redirect("/register")

        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, FALSE)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()

        return redirect("/")
        
@app.route("/profile")
def profile():
    return render_template("profile.html")