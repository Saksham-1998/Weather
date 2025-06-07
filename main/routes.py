from main import app
from main.models import User
from main.forms import RegisterForm, LoginForm
from main import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash


from flask import render_template, request, jsonify, url_for, flash, redirect
import json
import os


@app.route('/', methods=['GET', 'POST'])
def index():
    register_form = RegisterForm(prefix='register')
    login_form = LoginForm(prefix='login')

    if register_form.validate_on_submit() and 'register-submit' in request.form:
        user = User(username=register_form.username.data,
                    email=register_form.email.data,
                    password_hash=generate_password_hash(register_form.password1.data))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Account created successfully! You are logged in', category='success')
        return redirect(url_for('weather'))

    elif login_form.validate_on_submit() and 'login-submit' in request.form:
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and check_password_hash(user.password_hash, login_form.password.data):
            login_user(user)
            flash('Login successful!', category='success')
            return redirect(url_for('weather'))
        else:
            flash('Invalid username or password', category='danger')

    return render_template('index.html', register_form=register_form, login_form=login_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out!", category="info")
    return redirect(url_for('index'))

@app.route('/weather')
@login_required
def weather():
    return render_template('weather.html')


def get_user_history_file():
    return f'history_{current_user.id}.json'


def load_history():
    history_file = get_user_history_file()

    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return []

def save_history(history):
    history_file = get_user_history_file()
    with open(history_file, 'w') as file:
        json.dump(history, file)

@app.route('/history', methods=['POST'])
@login_required
def add_city():
    city = request.json.get('city')
    history = load_history()
    if city and city not in history:
        history.insert(0, city)
        if len(history) > 10:
            history = history[:10]
        save_history(history)
    return jsonify({'status': 'success'})

@app.route('/history_page')
@login_required
def history_page():
    history = load_history()
    return render_template('history.html', history=history)