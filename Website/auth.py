from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged In Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not match', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 1 and len(user_name) < 1 and len(password1) < 1:
            flash('Please fill out the form', category='error')
        elif len(email) < 4:
            flash('Please enter valid Email', category='error')
        elif len(user_name) < 2:
            flash('User name is too short', category='error')
        elif password1 != password2:
            flash('Please confirm password', category='error')
        elif len(password1) < 6:
            flash('Password is too short', category='error')
        else:
            new_user = User(email=email, user_name=user_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(user, remember=True)
            flash('Account Created!', category='success')
            # return redirect('/') will do but in case the url was changed it's better this way
            return redirect(url_for('auth.login'))

    return render_template("sign-up.html", user=current_user)
