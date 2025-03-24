from flask import Flask,render_template,redirect,request
from flask import current_app as app
from models.model1 import *

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
                    return render_template("user.html")
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

@app.route("/chapter/<name>",methods=["GET","POST"])
def chapter(name):
    if request.method=="POST":
        action = request.form.get("action")
        if action=="SAVE":
            chapter_name = request.form.get("chapter")
            sub_id = (Subject.query.filter_by(subject_name=name).first()).id
            new_chapter = Chapter(chapter_name=chapter_name,subject_id=sub_id)
            db.session.add(new_chapter)
            db.session.commit()
            return redirect("/home")
        else:
            return redirect("/home")
    return render_template("new_chapter.html",sub_name=name)

@app.route("/quiz_home",methods=["GET","POST"])
def quiz_home():
    chapter_info = Chapter.query.all()
    return render_template("quiz_management.html",chapter_info=chapter_info)

@app.route("/quiz/<name>",methods=["GET","POST"])
def quiz(name):
    if request.method=="POST":
        action = request.form.get("action")
        if action=="SAVE":
            quiz_name = request.form.get("quiz")
            duration = request.form.get("duration")
            deadline = request.form.get("deadline")
            chap_id = (Chapter.query.filter_by(chapter_name=name).first()).id
            new_quiz = Quiz(quiz_name=quiz_name,chapter_id=chap_id,deadline=deadline,duration=duration)
            db.session.add(new_quiz)
            db.session.commit()
            return redirect("/quiz_home")
        else:
            return redirect("/quiz_home")
    return render_template("new_quiz.html",chap_name=name)

@app.route("/question/<name>",methods=["GET","POST"])
def question(name):
    if request.method=="POST":
        action = request.form.get("action")
        if action=="SAVE":
            qno = request.form.get("qno")
            qstatement = request.form.get("q")
            quiz_id = (Quiz.query.filter_by(quiz_name=name).first()).id
            answer = request.form.get("answer")
            option1 = request.form.get("option1")
            option2 = request.form.get("option2")
            option3 = request.form.get("option3")
            option4 = request.form.get("option4")
            new_question = Question(qno=qno,quiz_id=quiz_id,question_statement=qstatement,correct_option=answer,option1=option1,option2=option2,option3=option3,option4=option4)
            db.session.add(new_question)
            db.session.commit()
            return redirect("/quiz_home")
        else:
            return redirect("/quiz_home")
    return render_template("new_question.html",quiz_name=name)

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