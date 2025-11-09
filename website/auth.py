from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)
SCHOOL_ID = "211"
    

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
     if request.method == 'POST':
        name = request.form.get('name')
        class_level = request.form.get('class_level')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')

        
        
        if len(name) < 4:
            flash('name is too short.', category='error')
        elif len(email) < 5:
            flash('Email is too short.', category='error')
        elif len(phone) < 10:
            flash('Phone number must be more than 10 digits.')
        elif len(password) < 5:
            flash('Password is too short')
        else:

         existing_user = User.query.filter_by(phone=phone).first()

        if existing_user:
         flash('Phone number already exists.', category='error')
        
     # Get the last 3 digits of the phone
        phone_suffix = phone[-4:]

        # Generate student ID based on pattern
        student_id = f"{SCHOOL_ID}{class_level}{phone_suffix}".upper()

        # Ensure the ID is unique (in case of same phone suffix)
        count = 1
        base_id = student_id
        while User.query.filter_by(student_id=student_id).first():
            count += 1
            student_id = f"{base_id}{count}"

        # Save new user
        new_user = User(
            name=name,
            class_level=class_level,
            phone=phone,
            email=email,
            password=generate_password_hash(password, method="pbkdf2:sha256"),
            student_id=student_id
            )
        db.session.add(new_user)
        db.session.commit()

        flash(f'Account created successfully! Your Student ID is {student_id}', category='success')
        return redirect(url_for('auth.login'))

     return render_template('sign_up.html')


@auth.route('/logout')
def logout():
    return "<p> Log out</p>"

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        student_id = request.form.get('student_id')
        password = request.form.get('password')

        user = User.query.filter_by(student_id=student_id).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('ID does not exist.', category='error')

    return render_template("login.html", boolean=True)


@auth.route('/nursery')
def nursery():
    return render_template('nursery.html')

@auth.route('/primary')
def primary():
    return render_template("primary.html")

@auth.route('/secondary')
def secondary():
    return render_template('secondary.html')

@auth.route('/skills')
def skills():
    return render_template('skills.html')

@auth.route('/graduation')
def graduation():
    return render_template('grad.html')