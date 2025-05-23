from flask import Flask,render_template,redirect,request
from flask import current_app as app
from models.model1 import *
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user")
        pwd = request.form.get("password")
        check = User.query.filter_by(username=user).first()
        if check:
            if check.password==pwd:
                if check.id==1: #admin id is 1.
                    return redirect("/home")
                else:
                    return redirect(f"/user/{user}")
            else:
                return render_template("login.html", error="Incorrect password. Please try again.")

        else:
            return render_template("login.html", error="User doesn't exist. Please Signup.")

    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = request.form.get("user")
        email = request.form.get("email")
        pwd = request.form.get("password")
        check = User.query.filter_by(username=user).first()
        if check:
            return render_template("register.html",error="User already exist, Try Login.")
        else:
            new_user = User(username=user,email=email,password=pwd)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html",msg="Registered Successfully.")
    return render_template("register.html")

@app.route("/home",methods=["GET","POST"])
def home():
    subject_info = Subject.query.all()
    return render_template("admin.html",subject_info=subject_info)

@app.route("/subject",methods=["GET","POST"])
def subject():
    if request.method=="POST":
        action = request.form.get("action")
        if action=="SAVE":
            subject_name = request.form.get("subject")
            subject_desc = request.form.get("description")
            new_subject = Subject(subject_name=subject_name,sub_description=subject_desc)
            db.session.add(new_subject)
            db.session.commit()
            return redirect("/home")
        else:
            return redirect("/home")
    return render_template("new_subject.html")

@app.route("/chapter/<int:id>",methods=["GET","POST"])
def chapter(id):
    if request.method=="POST":
        action = request.form.get("action")
        if action=="SAVE":
            chapter_name = request.form.get("chapter")
            new_chapter = Chapter(chapter_name=chapter_name,subject_id=id)
            db.session.add(new_chapter)
            db.session.commit()
            return redirect("/home")
        else:
            return redirect("/home")
    return render_template("new_chapter.html",sub_id=id)

@app.route("/quiz_home",methods=["GET","POST"])
def quiz_home():
    chapter_info = Chapter.query.all()
    return render_template("quiz_management.html",chapter_info=chapter_info)

@app.route("/quiz/<int:id>",methods=["GET","POST"])
def quiz(id):
    if request.method=="POST":
        action = request.form.get("action")
        if action=="SAVE":
            quiz_name = request.form.get("quiz")
            duration = request.form.get("duration")
            deadline = request.form.get("deadline")
            new_quiz = Quiz(quiz_name=quiz_name,chapter_id=id,deadline=deadline,duration=duration)
            db.session.add(new_quiz)
            db.session.commit()
            return redirect("/quiz_home")
        else:
            return redirect("/quiz_home")
    return render_template("new_quiz.html",chap_id=id)

@app.route("/question/<int:id>",methods=["GET","POST"])
def question(id):
    if request.method=="POST":
        action = request.form.get("action")
        if action=="SAVE":
            qno = request.form.get("qno")
            qstatement = request.form.get("q")
            answer = request.form.get("answer")
            option1 = request.form.get("option1")
            option2 = request.form.get("option2")
            option3 = request.form.get("option3")
            option4 = request.form.get("option4")
            new_question = Question(qno=qno,quiz_id=id,question_statement=qstatement,correct_option=answer,option1=option1,option2=option2,option3=option3,option4=option4)
            db.session.add(new_question)
            db.session.commit()
            return redirect(f"/question/{id}")
        else:
            return redirect("/quiz_home")
    return render_template("new_question.html",quiz_name=id)

@app.route("/sub_search")
def sub_search():
    query = request.args.get("query", "").strip().lower()
    subject_info = Subject.query.filter(Subject.subject_name.ilike(f"%{query}%")).all()
    return render_template("admin.html",query=query,subject_info=subject_info)

@app.route("/chap_search")
def chap_search():
    query = request.args.get("query", "").strip().lower()
    chapter_info = Chapter.query.filter(Chapter.chapter_name.ilike(f"%{query}%")).all()
    return render_template("quiz_management.html",query=query,chapter_info=chapter_info)

@app.route("/user/<username>",methods=["GET","POST"])
def user(username):
    user_info = User.query.filter_by(username=username).first()
    quiz_info = Quiz.query.all()
    attempt = QuizAttempt.query.filter_by(user_id=user_info.id).all()
    quiz_ids=[]
    for q in attempt:
        quiz_ids.append(q.quiz_id)
    return render_template("user.html",quiz_info=quiz_info,user=username,attempted=quiz_ids)

@app.route("/quiz_search/<username>")
def quiz_search(username):
    user_info = User.query.filter_by(username=username).first()
    attempt = QuizAttempt.query.filter_by(user_id=user_info.id).all()
    quiz_ids=[]
    for q in attempt:
        quiz_ids.append(q.quiz_id)
    query = request.args.get("query", "").strip().lower()
    quiz_info = Quiz.query.filter(Quiz.quiz_name.ilike(f"%{query}%")).all()
    return render_template("user.html",query=query,quiz_info=quiz_info,user=username,attempted=quiz_ids)

@app.route("/view/<int:id>/<username>",methods=["GET","POST"])
def view(id,username):
    quiz_info = Quiz.query.filter_by(id=id).first()
    return render_template("view.html",quiz=quiz_info,user=username)

@app.route("/start/<int:id>/<username>",methods=["GET","POST"])
def start(id,username):
    user_info = User.query.filter_by(username=username).first()
    new_attempt = QuizAttempt(user_id=user_info.id,quiz_id=id)
    db.session.add(new_attempt)
    db.session.commit()
    question_info = Question.query.filter_by(quiz_id=id).all()
    quiz_info = Quiz.query.filter_by(id=id).first()
    return render_template("start.html",question_info=question_info,user=username,quiz=quiz_info,attempt_id=new_attempt.id)

@app.route("/scores/<username>", defaults={"id": None,"attempt_id":None}, methods=["GET", "POST"])
@app.route("/scores/<int:id>/<username>/<int:attempt_id>",methods=["GET","POST"])
def scores(id,username,attempt_id):
    if request.method=="POST":
        question_info = Question.query.filter_by(quiz_id=id).all()
        submitted_answers = {int(key): int(request.form.get(key, 0)) for key in request.form.keys()}
        for qno,ans in submitted_answers.items():
            quest = Question.query.filter_by(qno=qno,quiz_id=id).first()
            new_response = UserResponse(quiz_attempt_id=attempt_id,question_id=quest.id,chosen_option=ans)
            db.session.add(new_response)
        db.session.commit()
        score = 0
        for q in question_info:
            if q.correct_option == submitted_answers[q.qno]:
                score = score+1
        attempt = QuizAttempt.query.filter_by(id=attempt_id).first()
        attempt.score = score
        db.session.commit()
    user_info = User.query.filter_by(username=username).first()
    attempt = QuizAttempt.query.filter_by(user_id=user_info.id).all()
    return render_template("scores.html",user=username,all_attempt=attempt)

@app.route("/view_attempt/<int:id>/<username>",methods=["GET","POST"])
def view_attempt(id,username):
    attempt = QuizAttempt.query.filter_by(id=id).first()
    response = UserResponse.query.filter_by(quiz_attempt_id=id).all()
    return render_template("view_attempt.html",response_info=response,user=username,attempt=attempt)

@app.route("/edit_subject/<int:id>",methods=["GET","POST"])
def edit_subject(id):
    subject = Subject.query.filter_by(id=id).first()
    if request.method=="POST":
        action = request.form.get("action")
        if action=="SAVE":
            subject.subject_name = request.form.get("subject")
            subject.sub_description = request.form.get("description")
            db.session.commit()
            return redirect("/home")
        else:
            return redirect("/home")
    return render_template("edit_subject.html",subject=subject)

@app.route("/delete_subject/<int:id>",methods=["GET","POST"])
def delete_subject(id):
    subject = Subject.query.filter_by(id=id).first()
    db.session.delete(subject)
    db.session.commit()
    return redirect("/home")

@app.route("/edit_chapter/<int:id>",methods=["GET","POST"])
def edit_chapter(id):
    chapter = Chapter.query.filter_by(id=id).first()
    if request.method=="POST":
        action = request.form.get("action")
        if action=="SAVE":
            chapter.chapter_name = request.form.get("chapter")
            db.session.commit()
            return redirect("/home")
        else:
            return redirect("/home")
    return render_template("edit_chapter.html",chapter=chapter)

@app.route("/delete_chapter/<int:id>",methods=["GET","POST"])
def delete_chapter(id):
    chapter = Chapter.query.filter_by(id=id).first()
    db.session.delete(chapter)
    db.session.commit()
    return redirect("/home")

@app.route("/edit_quiz/<int:id>",methods=["GET","POST"])
def edit_quiz(id):
    quiz = Quiz.query.filter_by(id=id).first()
    if request.method=="POST":
        action = request.form.get("action")
        if action=="SAVE":
            quiz.quiz_name = request.form.get("quiz")
            quiz.duration = request.form.get("duration")
            quiz.deadline = request.form.get("deadline")
            db.session.commit()
            return redirect("/quiz_home")
        else:
            return redirect("/quiz_home")
    return render_template("edit_quiz.html",quiz=quiz)

@app.route("/delete_quiz/<int:id>",methods=["GET","POST"])
def delete_quiz(id):
    quiz = Quiz.query.filter_by(id=id).first()
    db.session.delete(quiz)
    db.session.commit()
    return redirect("/quiz_home")

@app.route("/view_quest/<int:quiz_id>",methods=["GET","POST"])
def view_quest(quiz_id):
    question_info = Question.query.filter_by(quiz_id=quiz_id).all()
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    return render_template("view_quest.html",quiz=quiz,question_info=question_info)

@app.route("/edit_quest/<int:id>",methods=["GET","POST"])
def edit_quest(id):
    question = Question.query.filter_by(id=id).first()
    quiz_id = question.quiz_id
    if request.method=="POST":
        action = request.form.get("action")
        if action=="SAVE":
            question.qno = request.form.get("qno")
            question.question_statement = request.form.get("q")
            question.correct_option = request.form.get("answer")
            question.option1 = request.form.get("option1")
            question.option2 = request.form.get("option2")
            question.option3 = request.form.get("option3")
            question.option4 = request.form.get("option4")
            db.session.commit()
            return redirect(f"/view_quest/{quiz_id}")
        else:
            return redirect(f"/view_quest/{quiz_id}")
    return render_template("edit_quest.html",question=question)

@app.route("/delete_quest/<int:id>",methods=["GET","POST"])
def delete_quest(id):
    question = Question.query.filter_by(id=id).first()
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    return redirect(f"/view_quest/{quiz_id}")

@app.route("/generate_chart/<name>",methods=["GET","POST"])
def generate_chart(name):
    if name=="admin":
        user_count = (
        db.session.query(
            Quiz.quiz_name,
            db.func.count(QuizAttempt.id).label("user_count")
        )
        .join(QuizAttempt, Quiz.id == QuizAttempt.quiz_id)
        .group_by(Quiz.quiz_name)
        .all()
        )

        df = pd.DataFrame(user_count, columns=["quiz", "user_count"])
        plt.figure(figsize=(10, 5))
        bars = plt.bar(df["quiz"], df["user_count"], color=["#4B0082", "#008080", "#2E8B57", "#32CD32"])
        plt.title("Quiz-wise Number of Users", fontsize=14, fontweight="bold")
        plt.xlabel("Quiz", fontsize=12)
        plt.ylabel("Number of Users", fontsize=12)
        plt.savefig("static/top_scores_chart.png")
        plt.close()
        return render_template("admin_summary.html")
    else:
        top_scores = (
        db.session.query(
            Quiz.quiz_name,
            db.func.max(QuizAttempt.score).label("top_score")
        )
        .join(QuizAttempt, Quiz.id == QuizAttempt.quiz_id)
        .group_by(Quiz.quiz_name)
        .all()
        )

        df = pd.DataFrame(top_scores, columns=["quiz", "topscore"])
        plt.figure(figsize=(10, 5))
        bars = plt.bar(df["quiz"], df["topscore"], color=["#4B0082", "#008080", "#2E8B57", "#32CD32"])
        plt.title("Quiz-wise Top Scores", fontsize=14, fontweight="bold")
        plt.xlabel("Quiz", fontsize=12)
        plt.ylabel("Top Score", fontsize=12)
        plt.savefig("static/top_scores_chart.png")
        plt.close()
        return render_template("summary.html",user=name)

@app.route("/user_details",methods=["GET","POST"])
def user_details():
    users = User.query.all()
    return render_template("user_details.html",users=users)

@app.route("/user_search")
def user_search():
    query = request.args.get("query", "").strip().lower()
    user_info = User.query.filter(User.username.ilike(f"%{query}%")).all()
    return render_template("user_details.html",query=query,users=user_info)