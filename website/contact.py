from flask import Blueprint, render_template, flash, request

contact_bp = Blueprint('contact', __name__)

@contact_bp.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        phone = request.form.get('phone')
        flash('Message received successfully!', 'success')
    return render_template('contact.html')