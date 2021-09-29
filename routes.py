from app import app 
from db import db
from flask import render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint, shuffle
from forms import RegisterForm, LoginForm

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
    sql = "SELECT U.username, CEILING((CAST(COUNT(*) FILTER (where O.correct) AS FLOAT) / COUNT(*)) * 100) AS correct_percentage, COUNT(*) AS total " \
          "FROM  answers A INNER JOIN options O ON A.option_id = O.id LEFT JOIN users U ON U.id = A.user_id " \
          "GROUP BY U.username ORDER BY correct_percentage DESC, total LIMIT 20"
    query_result = db.session.execute(sql)
    scores = query_result.fetchall() 
    return render_template("scoreboard.html", scores=scores)

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/")

    if request.method == "GET":
        form = LoginForm()
    else:
        form = LoginForm(request.form)
        if form.validate_on_submit():      
            sql = "SELECT id, password FROM users WHERE username=:username"
            result = db.session.execute(sql, {"username": form.username.data})
            user = result.fetchone()
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
            sql = "SELECT username FROM users WHERE username=:username"
            result = db.session.execute(sql, {"username": form.username.data})
            user = result.fetchone()
    
            if user:
                flash("Käyttäjänimi on jo käytössä", "danger")
                return render_template("register.html", form=form)
    
            hash_value = generate_password_hash(form.password.data)
            sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, FALSE)"
            db.session.execute(sql, {"username":form.username.data, "password":hash_value})
            db.session.commit()
            flash(f"Käyttäjätunnus luotu käyttäjälle {form.username.data}", "success")
    
            return redirect("/")

    return render_template("register.html", form=form)
        
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