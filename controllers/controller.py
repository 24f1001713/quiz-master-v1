from flask import Flask,render_template,redirect,request
from flask import current_app as app
from models.model1 import *

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