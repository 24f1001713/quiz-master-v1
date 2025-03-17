from controllers.database import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(),unique=True,nullable=False)
    email = db.Column(db.String(),unique=True,nullable=False)
    password = db.Column(db.String(),nullable=False)
    score_details = db.relationship("Scores",backref="user_details")

class Subject(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    subject_name = db.Column(db.String(),unique=True,nullable=False)
    sub_description = db.Column(db.String(),nullable=False)
    chap_details = db.relationship("Chapter",backref="sub_details")

class Chapter(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    chapter_name = db.Column(db.String(),unique=True,nullable=False)
    subject_id = db.Column(db.Integer,db.ForeignKey("subject.id"),nullable=False)
    quiz_details = db.relationship("Quiz",backref="chapter_details")

class Quiz(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    quiz_name = db.Column(db.String(),unique=True,nullable=False)
    chapter_id = db.Column(db.Integer,db.ForeignKey("chapter.id"),nullable=False)
    deadline = db.Column(db.String(),nullable=False)
    duration = db.Column(db.String(),nullable=False)
    question_details = db.relationship("Question",backref="quiz_details")
    score_details = db.relationship("Scores",backref="quiz_details")

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qno = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column(db.Integer,db.ForeignKey("quiz.id"),nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(), nullable=False)
    option2 = db.Column(db.String(), nullable=False)
    option3 = db.Column(db.String(), nullable=False)
    option4 = db.Column(db.String(), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    quiz_id = db.Column(db.Integer,db.ForeignKey("quiz.id"),nullable=False)
