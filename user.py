from settings import app
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


def create_user(_username, _password):
    new_user = User(username = _username ,  password= _password)
    db.session.add(new_user)
    db.session.commit()

def get_all_user():
    return User.query.all()


def __repr__(self):
    user_object = {
        'username': self.username,
        'password': self.password
    }
    return json.dumps(user_object)


def username_password_match(_username, _password):
    user = User.query.filter_by(username=_username).filter_by(password=_password).first()
    if user is None:
        return False
    else:
        return True



