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



class Event(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

class NoticeBoard(db.Model, UserMixin):
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

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_per_student = db.Column(db.Integer, nullable=False)

class TermRevenue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term_name = db.Column(db.String(50), nullable=False)
    session_year = db.Column(db.String(10), nullable=False)
    amount_per_student = db.Column(db.Integer, nullable=False)
    num_students = db.Column(db.Integer, nullable=False)
    amount_expected = db.Column(db.Integer, nullable=False)
    amount_collected = db.Column(db.Integer, nullable=False)
    amount_remaining = db.Column(db.Integer, nullable=False)
    date_closed = db.Column(db.DateTime, nullable=False)







    

