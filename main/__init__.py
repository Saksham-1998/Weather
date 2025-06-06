from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstdata.db'
app.config['SECRET_KEY'] = 'f2e38c2cc98ed437985ef618d6fc602d'

db= SQLAlchemy(app)

from main.models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 
login_manager.login_message_category= 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from main import routes

with app.app_context():
    db.create_all()