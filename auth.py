from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from models import User
from bcrypt import hashpw, checkpw, gensalt

db = SQLAlchemy()

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/')
def index():
    return render_template('client.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not checkpw(password.encode('utf-8'), user.password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    return redirect(url_for('auth.index'))


@auth.route('/signup')
def signup():
    return render_template('register.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    new_user = User(email=email, username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@ auth.route('/logout')
def logout():
    return 'logout'
