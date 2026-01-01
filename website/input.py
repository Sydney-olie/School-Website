from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import db
from .models import User
from .models import NoticeBoard
from .models import Payment
from datetime import datetime
import os
from dotenv import load_dotenv
import requests



load_dotenv()
input = Blueprint('input', __name__)

@input.route('/admindashboard')
def admindashboard():
     return render_template('/admin/admindashboard.html')

@input.route('/adminpayments', methods=['GET', 'POST'])
def adminpayments():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        amount_paid = request.form.get('amount_paid')
        date_paid = request.form.get('date_paid')
        balance = request.form.get('balance')

        # Check if student exists
        user = User.query.filter_by(student_id=student_id).first()
        if not user:
            flash("Student ID not found!", "danger")
            return redirect(url_for('input.adminpayments'))

        # Convert date to datetime format
        try:
            date_paid = datetime.strptime(date_paid, "%Y-%m-%d").date()
        except:
            flash("Invalid date format!", "danger")
            return redirect(url_for('input.adminpayments'))

        # Save payment
        payment = Payment(
            student_id=student_id,
            amount_paid=float(amount_paid),
            date_paid=date_paid,
            balance=float(balance)
        )

        db.session.add(payment)
        db.session.commit()

        flash("Payment added successfully!", "success")
        return redirect(url_for('input.adminpayments'))

    return render_template('/admin/adminpayments.html')


@input.route('/search', methods=['GET'])
def search():
    student_id = request.args.get('student_id')
    if not student_id:
        return "Please enter a student ID"
# IMPORTANT: search by student_id column, NOT id
    student = User.query.filter_by(student_id=student_id).first()
    if not student:
        return "No student found with that ID"

    return redirect(url_for('input.student_profile', student_id=student.student_id))
     
 

@input.route('/adminstudent_profile/<student_id>')
def student_profile(student_id):
    user = User.query.filter_by(student_id=student_id).first_or_404()
    payments = Payment.query.filter_by(student_id=student_id).all()
    notice = (NoticeBoard.query.order_by(NoticeBoard.id.desc()).first())
    return render_template("/admin/adminstudent_profile.html", user=user, payments=payments, notice=notice)

input.route('/profile/<str:student_id')
def profile(student_id):
    user = User.query.filter_by(student_id=student_id).first_or_404()
    payments = Payment.query.filter_by(student_id=student_id).all()
    notice = (NoticeBoard.query.order_by(NoticeBoard.id.desc()).first())
    return render_template("/admin/adminstudent_profile.html", user=user, payments=payments, notice=notice)

@input.route('/notice', methods=['GET', 'POST'])
def notice():
    if request.method == 'POST':
        content = request.form['content']
        new_notice_item = NoticeBoard(content=content)
        db.session.add(new_notice_item)
        db.session.commit()
    flash("notice added Successfully", "success")
    notice = NoticeBoard.query.all() 

    return render_template('/admin/notice.html', notice=notice)

@input.route('/payment')
def payment():
    return render_template("payment.html")

@input.route('/revenue', methods=['GET', 'POST'])
def revenue():
        total_students = User.query.count()
        #default amount per term
        amount_per_student = None
        estimated_income = None
        collected_amount = None
        outstanding_amount = None

        if request.method == 'POST':
            amount_per_student = int(request.form['amount'])
            #calculate estimated income
            estimated_income = total_students * amount_per_student
            #Calculate amount recieved
            collected_amount = db.session.query(db.func.sum(Payment.amount_paid)).scalar() or 0
            #calculate oustanding balance
            outstanding_amount = estimated_income - collected_amount

        return render_template('revenue.html',
                               total_students=total_students,
                               amount_per_student=amount_per_student,
                               estimated_income=estimated_income,
                               collected_amount=collected_amount,
                               outstanding_amount=outstanding_amount)
