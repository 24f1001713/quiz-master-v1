from flask import Flask
from controllers.database import db

app=None

def create_app():
    app=Flask(__name__)
    app.debug=True
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///quiz.sqlite3" #3 database connection for flask app
    db.init_app(app) #used to bind sqlalchemy object with flask app
    app.app_context().push()
    return app

app = create_app()

from controllers.controller import * #2

if __name__=="__main__":
    app.run()