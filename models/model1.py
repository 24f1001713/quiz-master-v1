from controllers.database import db

class User(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(),unique=True,nullable=False)
    email=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    type=db.Column(db.String(),default="general")

class Subject(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    subject = db.Column(db.String(),unique=True,nullable=False)
    sub_id = db.Column(db.String(),unique=True,nullable=False)
    chap_details = db.relationship("Chapter",backref="sub_details")

class Chapter(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    chapter = db.Column(db.String(),unique=True,nullable=False)
    subject = db.Column(db.String(),db.ForeignKey("subject.subject"),nullable=False)
