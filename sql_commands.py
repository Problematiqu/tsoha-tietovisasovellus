from db import db

def add_answer(id: int, user: int):
    sql = "INSERT INTO answers (option_id, user_id) VALUES (:option, :user)"
    db.session.execute(sql, {"option": id, "user": user})
    db.session.commit()

def add_user(username: str, hash_value):
    sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, FALSE)"
    db.session.execute(sql, {"username": username, "password":hash_value})
    db.session.commit()

def add_question(question: str, topic: int, correct_option: str, options: list):
    sql = "INSERT INTO questions (question, topic_id) VALUES (:question, :topic) RETURNING id"
    query_result = db.session.execute(sql, {"question": question, "topic": topic})
    id = query_result.fetchone()[0]
    sql = "INSERT INTO options (option, correct, question_id) VALUES (:option, TRUE, :id)"
    db.session.execute(sql, {"option": correct_option, "id": id})
    for option in options:
        sql = "INSERT INTO options (option, correct, question_id) VALUES (:option, FALSE, :id)"
        db.session.execute(sql, {"option": option, "id": id})
    db.session.commit()

def add_quiz(id: int, quiz: int):
    sql = "INSERT INTO quiz (user_id, question) VALUES (:id, :quiz)"
    db.session.execute(sql, {"id": id, "quiz": quiz})
    db.session.commit()

def delete_quiz(id: int):
    sql = "DELETE FROM quiz WHERE user_id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()

def get_admin(id: int):
    sql = "SELECT admin FROM users WHERE id=:id"
    query_result = db.session.execute(sql, {"id": id})
    return query_result.fetchone()[0]

def get_options(number: int):
    sql = "SELECT Q.question, O.option, O.id FROM questions Q LEFT JOIN options O ON Q.id = O.question_id WHERE Q.id=:number"
    query_result = db.session.execute(sql, {"number": number}) 
    return query_result.fetchall()

def get_scoreboard():
    sql = "SELECT U.username, CEILING((CAST(COUNT(*) FILTER (where O.correct) AS FLOAT) / COUNT(*)) * 100) AS correct_percentage, COUNT(*) AS total " \
          "FROM  answers A INNER JOIN options O ON A.option_id = O.id LEFT JOIN users U ON U.id = A.user_id " \
          "GROUP BY U.username ORDER BY correct_percentage DESC, total LIMIT 20"
    query_result = db.session.execute(sql)
    return query_result.fetchall() 

def get_user(username: str):
    sql = "SELECT id, password FROM users WHERE username=:username"
    query_result = db.session.execute(sql, {"username": username})
    return query_result.fetchone()

def get_user_scores(id: int):
    sql = "SELECT T.id, T.topic, COUNT(*) FILTER (where O.correct) AS correct, COUNT(*) AS total " \
          "FROM answers A INNER JOIN options O on A.option_id = O.id INNER JOIN questions Q on Q.id = O.question_id RIGHT JOIN topic T ON T.id = Q.topic_id " \
          "WHERE A.user_id =:user_id  GROUP BY T.id"
    query_result = db.session.execute(sql, {"user_id": id})
    return query_result.fetchall()

def get_quiz(id: int):
    sql = "SELECT question FROM quiz WHERE user_id=:id"
    query_result = db.session.execute(sql, {"id": id})
    return query_result.fetchall()

def get_topics():
    sql = "SELECT id, topic FROM topic"
    query_result = db.session.execute(sql)
    return query_result.fetchall()

def is_correct(id: int):
    sql = "SELECT correct FROM options WHERE id=:value"
    query_result = db.session.execute(sql, {"value": id})
    return query_result.fetchone()[0]

def question_count():
    sql = "SELECT COUNT(id) FROM questions"
    query_result = db.session.execute(sql)
    return query_result.fetchone()[0]












