from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)













class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    
class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_image = db.Column(db.Text, nullable = False)
    second_image = db.Column(db.Text, nullable = False)

class Evaluations(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    criteria_1 = db.Column(db.Integer)
    criteria_2 = db.Column(db.Integer)
    criteria_3 = db.Column(db.Integer)
    criteria_4 = db.Column(db.Integer)
    criteria_5 = db.Column(db.Integer)
    criteria_6 = db.Column(db.Integer)
    criteria_7 = db.Column(db.Integer)
    criteria_8 = db.Column(db.Integer)
    criteria_9 = db.Column(db.Integer)
    criteria_10 = db.Column(db.Integer)


class Eval_Count(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    total_Evals = db.Column(db.Integer)
    last_img_id = db.Column(db.Integer)
