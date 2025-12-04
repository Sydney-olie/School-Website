from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    class_level = db.Column(db.String(10), nullable=False)


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(20), nullable=False)
    admin_password = db.Column(db.String(100), nullable=False)

class TimetableDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)  # Monday, Tuesday...
    entries = db.relationship('TimetableEntry', backref='day_obj', lazy=True, cascade="all, delete")

class TimetableEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    end_time = db.Column(db.String(20), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('timetable_day.id'), nullable=False)

class Event(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

class Calender(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    content= db.Column(db.Text)
    

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount_paid = db.Column(db.Float)
    balance = db.Column(db.Float)
    date_paid = db.Column(db.Date)

class PaymentHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session = db.Column(db.String(20))
    term = db.Column(db.String(20))
    amount_paid = db.Column(db.Float)
    date_paid = db.Column(db.String(20))







    

