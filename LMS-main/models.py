from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(20))           # 'cs50p' or 'cs50ai'
    lecture_id = db.Column(db.String(50))       # e.g. 'lecture_1'
    slug = db.Column(db.String(50))             # e.g. 'indoor'
    title = db.Column(db.String(100))
    description = db.Column(db.Text)           # FULL description, not a summary
    check50_slug = db.Column(db.String(200))
    difficulty = db.Column(db.String(20))
    common_mistakes = db.Column(db.Text)       # JSON-encoded list of strings

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))
    code = db.Column(db.Text)
    passed = db.Column(db.Boolean, default=False)
    tests_passed = db.Column(db.Integer, default=0)
    tests_failed = db.Column(db.Integer, default=0)
    raw_output = db.Column(db.Text)            # Raw check50 terminal output — never trim this
    submitted_at = db.Column(db.DateTime, default=db.func.now())
