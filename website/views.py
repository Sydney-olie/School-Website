from flask import Blueprint, render_template
views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("index.html")

@views.route('/nursery')
def nursery():
    return render_template('nursery.html')

@views.route('/primary')
def primary():
    return render_template("primary.html")

@views.route('/secondary')
def secondary():
    return render_template('secondary.html')

@views.route('/skills')
def skills():
    return render_template('skills.html')

@views.route('/graduation')
def graduation():
    return render_template('grad.html')

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')

@views.route('/logout')
def logout():
    return render_template('home.html')

@views.route('/nav')
def nav():
    return render_template('navigation.html')

@views.route('/contact')
def contact():
    return render_template('contact.html')



