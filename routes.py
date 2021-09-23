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
        sql = "SELECT Q.question, O.option, O.id FROM questions Q LEFT JOIN options O ON Q.id = O.question_id WHERE Q.id=:number"
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
        if "user_id" in session:
            sql = "INSERT INTO answers (option_id, user_id) VALUES (:option, :user)"
            db.session.execute(sql, {"option": value, "user": session["user_id"]})
            db.session.commit()

    return render_template("finish.html", score=correct_answers)


@app.route("/scoreboard")
def scoreboard():
    sql = "SELECT U.username, (CAST(COUNT(*) FILTER (where O.correct) AS FLOAT) / COUNT(*)) * 100 AS average, COUNT(*) AS total " \
          "FROM  answers A INNER JOIN options O ON A.option_id = O.id LEFT JOIN users U ON U.id = A.user_id " \
          "GROUP BY U.username ORDER BY average DESC, total LIMIT 20"
    query_result = db.session.execute(sql)
    scores = query_result.fetchall() 
    return render_template("scoreboard.html", scores=scores)

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username": username})
        user = result.fetchone()
        if not user:
            flash("Tunnus tai salasana olivat väärin")
            return redirect("/login")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["user_id"] = user.id
                return redirect("/")
            else:
                flash("Käyttäjätunnus tai salasana olivat vääriä")
                return redirect("/login")

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
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
    if "user_id" not in session:
        return redirect("/")

    sql = "SELECT T.id, T.topic, COUNT(*) FILTER (where O.correct) AS correct, COUNT(*) AS total FROM answers A " \
          "INNER JOIN options O on A.option_id = O.id INNER JOIN questions Q on Q.id = O.question_id INNER JOIN topic T ON T.id = Q.topic_id " \
          "WHERE A.user_id =:user_id  GROUP BY T.id"
    query_result = db.session.execute(sql, {"user_id":session["user_id"]})
    scores = query_result.fetchall()
    return render_template("profile.html", scores=scores)