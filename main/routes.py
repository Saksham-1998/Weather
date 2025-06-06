from main import app
from main.models import User
from main.forms import RegisterForm, LoginForm
from main import db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash


from flask import render_template, request, jsonify, url_for, flash, redirect
import json
import os



@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterForm()
    if form.validate_on_submit():
        user_create = User(username= form.username.data,
                           email= form.email.data,
                           password_hash = generate_password_hash(form.password1.data))
        db.session.add(user_create)
        db.session.flush()
        db.session.commit()

        login_user(user_create)
        flash('Account created successfully! You are logged in', category='success')
        return redirect(url_for('weather'))
    
    if form.errors != {}:
        for field, error_messages in form.errors.items():
            for err in error_messages:
                flash(f"{field.capitalize()}: {err}", category='danger')
    
    return render_template('index.html', form = form)

@app.route('/weather')
@login_required
def weather():
    return render_template('weather.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', category='success')
            return redirect(url_for('weather'))   
        else:
            flash('Invalid username or password', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out!", category="info")
    return redirect(url_for('login'))




HISTORY_FILE = 'history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as file:
            return json.load(file)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file)

@app.route('/history', methods=['POST'])
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
def history_page():
    history = load_history()
    return render_template('history.html', history=history)