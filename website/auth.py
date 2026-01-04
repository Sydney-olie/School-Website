from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Admin
import os
from dotenv import load_dotenv



load_dotenv()



auth = Blueprint('auth', __name__)
SCHOOL_ID = os.getenv("SCHOOL_ID")
SCHOOL_CODE= os.getenv("SCHOOL_CODE")
    

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
     if request.method == 'POST':
        name=  request.form.get('name')
        class_level = request.form.get('class_level')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        school_code = request.form.get('school_code')

        
        
        if len(name) < 4:
            flash('name is too short.', category='error')
        elif len(email) < 5:
            flash('Email is too short.', category='error')
        elif len(phone) < 10:
            flash('Phone number must be more than 10 digits.')
        elif len(password) < 5:
            flash('Password is too short')
        elif school_code != SCHOOL_CODE:
            flash('Invalid school code. Cannot create an account.')
        else:

         existing_user = User.query.filter_by(phone=phone).first()

        if existing_user:
         flash('Phone number already exists.', category='error')
        
     # Get the last 4 digits of the phone
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
                return redirect(url_for('input.student_profile', student_id=user.student_id))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('ID does not exist.', category='error')

    return render_template("login.html", boolean=True)


ADMIN_SCHOOL_CODE= os.getenv("ADMIN_SCHOOL_CODE")
@auth.route('/adminsignup', methods=['GET', 'POST'])
def adminsignup():
     if request.method == 'POST':
        admin_id =  request.form.get('admin_id')
        admin_password = request.form.get('admin_password')
        admin_school_code = request.form.get('admin_school_code')

        
        
        if len(admin_id) < 4:
            flash('Id is too short.', category='error')
        elif len(admin_password) < 5:
            flash('Password is too short.', category='error')
        elif admin_school_code != ADMIN_SCHOOL_CODE:
            flash('Invalid Admin school code. Cannot create an account.')
        else:

         existing_admin = Admin.query.filter_by(admin_id=admin_id).first()

        if existing_admin:
         flash('Admin account already exists.', category='error')
        

        # Ensure the ID is unique (in case of same phone suffix)
        count = 1
        base_id = admin_id
        while Admin.query.filter_by(admin_id=admin_id).first():
            count += 1
            admin_id = f"{base_id}{count}"

        # Save new user
        new_admin = Admin(
            admin_id=admin_id,
            admin_password=generate_password_hash(admin_password, method="pbkdf2:sha256"),
            )
        db.session.add(new_admin)
        db.session.commit()

        flash(f'Account created successfully!', category='success')
        return redirect(url_for('auth.admin'))

     return render_template('/admin/adminsignup.html')


@auth.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        
        admin_id = request.form.get('admin_id')
        admin_password = request.form.get('admin_password')

        admin = Admin.query.filter_by(admin_id=admin_id).first()
        if admin:
            if check_password_hash(admin.admin_password, admin_password):
                flash('Logged in successfully!', category='success')
                return redirect(url_for('input.admindashboard'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('ID does not exist.', category='error')

    return render_template("/admin/adminlogin.html", boolean=True)





