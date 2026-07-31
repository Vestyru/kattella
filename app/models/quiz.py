from sqlalchemy import Null
from ..extensions import db
from datetime import datetime

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    kattell_id = db.Column(db.Integer, nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    options = db.relationship('Options', backref='question', lazy=True)


class Options(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    label = db.Column(db.Text)
    value = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answered_text = db.Column(db.Text)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)

    question = db.relationship('Questions', backref='answers', lazy=True)



class Participants(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(255))
    squad = db.Column(db.String(255))
    callsign = db.Column(db.String(255))
    date = db.Column(db.String(255))
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, default=datetime.utcnow)



class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'), nullable=False)
    scores_json = db.Column(db.Text, nullable=False)
    new_scores = db.Column(db.Text, nullable=False)
    group_user = db.Column(db.String(255), nullable=False, default=Null)
    group = db.Column(db.String(255), nullable=False)
    warnings_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    participant = db.relationship('Participants', backref='results')