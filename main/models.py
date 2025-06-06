from flask_login import UserMixin
from main import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    username= db.Column(db.String(length=50),nullable= False, unique= True)
    email= db.Column(db.String(length=100),nullable=True)
    password_hash= db.Column(db.String(length=100), nullable=False)

    def __repr__(self):
        return f"The name of the user is {self.username}"