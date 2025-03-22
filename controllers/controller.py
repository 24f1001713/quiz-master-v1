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
                    return render_template("admin.html")
                else:
                    return render_template("user.html")
            else:
                return "password is incorrect"

        else:
            return "user doesn't exist"

    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = request.form.get("user")
        email = request.form.get("email")
        pwd = request.form.get("password")
        check = User.query.filter_by(username=user).first()
        if check:
            return "user already exist"
        else:
            new_user = User(username=user,email=email,password=pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
    return render_template("register.html")

@app.route("/home",methods=["GET","POST"])
def home():
    return render_template("admin.html")

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
            sub_id=(Subject.query.filter_by(subject_name=name).first()).id
            new_chapter = Chapter(chapter_name=chapter_name,subject_id=sub_id)
            db.session.add(new_chapter)
            db.session.commit()
            return redirect("/home")
        else:
            return redirect("/home")
    return render_template("new_chapter.html",sub_name=name)