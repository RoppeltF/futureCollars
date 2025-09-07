# dbClasses.py
from extensions import db, bcrypt
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class UserDB(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(30), nullable=False)
    user_type = db.Column(db.String(30), nullable=False, default="user")  # "admin" ou "user"
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, email, first_name, last_name, mobile, user_type, password):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.mobile = mobile
        self.user_type = user_type
        self.set_password(password)

    @property
    def is_admin(self):
        return self.user_type == "admin"

    def set_password(self, password):
        #generate hashed password
        self.password = generate_password_hash(password)

    def check_password(self, password):
        #Validates password
        return check_password_hash(self.password, password)

    @classmethod
    def create_user(cls, username, email, first_name, last_name, mobile, user_type, password):
        #Creates and save User
        user = cls(username, email, first_name, last_name, mobile, user_type, password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_username(cls, username):
        #Search Username
        return cls.query.filter_by(username=username).first()

    @classmethod
    def validate_login(cls, username, password):
        #  Valites User Login
        user = cls.get_by_username(username)
        if user and user.check_password(password):
            return True
        return False


class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)

    def __init__(self, balance):
        self.balance = balance


class ItemDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(120), unique=True, nullable=False)
    item_price = db.Column(db.Integer, nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, item_name, item_price, item_quantity):
        self.item_name = item_name
        self.item_price = item_price
        self.item_quantity = item_quantity


class LOG(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable=False)

    def __init__(self, message, type):
        self.date = datetime.now()
        self.message = message
        self.type = type
