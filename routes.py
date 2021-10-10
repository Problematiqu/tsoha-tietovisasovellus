from app import app 
from flask import render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint, shuffle
from forms import AddForm, QuizForm, RegisterForm, LoginForm
import sql_commands

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    return render_template("start.html")

@app.route("/quiz", methods=["GET", "POST"]) 
def quiz():
    
    if "user_id" in session:
        remaining_questions = sql_commands.get_quiz(session["user_id"]) 

    if "user_id" in session and remaining_questions:
        question_ids = [question.question for question in remaining_questions]
        sql_commands.delete_quiz(session["user_id"])
    elif "questions" in session:
        question_ids = session["questions"]
    else:
        query = sql_commands.get_question_ids()
        question_ids = [question.id for question in query]
        shuffle(question_ids)
        question_ids = question_ids[0:10]

    questions = {}    
    for question_id in question_ids:
        options = sql_commands.get_options(question_id)
        shuffle(options)
        questions[question_id] = options

    if "user_id" in session:
        for question_id in question_ids:
            sql_commands.add_quiz(session["user_id"], question_id)
    else:
        session["questions"] = question_ids

    form = QuizForm()

    i = 0
    for question in questions:
        form.question[i].label = questions[question][0].question
        form.question[i].choices = [(questions[question][0].id, questions[question][0].option), (questions[question][1].id, questions[question][1].option), \
            (questions[question][2].id, questions[question][2].option), (questions[question][3].id, questions[question][3].option)]
        i += 1

    if form.validate_on_submit():
        data = form.question.data
        score = 0
    
        for value in data:
            correct = sql_commands.is_correct(value)
            if correct:
                score += 1
            if "user_id" in session:
                sql_commands.add_answer(value, session["user_id"])
        if "user_id" in session:
            sql_commands.delete_quiz(session["user_id"])
        if "questions" in session:
            del session["questions"]

        return render_template("finish.html", score=score)
    
    return render_template("quiz.html", form=form)

@app.route("/result", methods=["POST"])
def result():
    form = QuizForm(request.form)
    print(form.question.data)
    if form.validate_on_submit():
        results = request.form
        print(form.question.data)
        score = 0
    
        for key in results.keys():
            value = results.get(key)
            correct = sql_commands.is_correct(value)
            if correct:
                score += 1
            if "user_id" in session:
                sql_commands.add_answer(value, session["user_id"])
    
        if "user_id" in session:
            sql_commands.delete_quiz(session["user_id"])
    
        return render_template("finish.html", score=score)

    print(form.errors)
    return redirect("/quiz")

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
                    session["admin"] = sql_commands.get_admin(user.id)
                    if "questions" in session: 
                        del session["questions"]
                    flash(f"Kirjauduttu sisään käyttäjänä {form.username.data}", "success")
                    return redirect("/")
                else:
                    flash("Käyttäjätunnus tai salasana olivat vääriä", "danger")
                    return redirect("/login")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["admin"]
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

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session: 
        return redirect("/")
    
    admin = sql_commands.get_admin(session["user_id"])

    if not admin:
        return redirect("/")

    if request.method =="GET":
        form = AddForm()
    else:
        form = AddForm(request.form)
        if form.validate_on_submit():
            sql_commands.add_question(form.question.data, int(form.topic.data), form.correct.data, form.incorrect.data)
            flash(f"Kysymys '{form.question.data}' lisätty!", "success")
            return redirect("/add")
            
    return render_template("add.html", form=form)

