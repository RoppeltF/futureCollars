# main.py
from flask import Flask
from extensions import db, bcrypt
from flask_alembic import Alembic
from flask_login import LoginManager

from dbClasses import UserDB

from dotenv import load_dotenv
load_dotenv()

import dbClasses
from routes import bp

app = Flask(__name__)
app.register_blueprint(bp)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "super-secret-key"  # 🔑 mude depois

# inicializa extensões
db.init_app(app)
bcrypt.init_app(app)

alembic = Alembic()
alembic.init_app(app)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "app.login"

@login_manager.user_loader
def load_user(user_id):
    return UserDB.query.get(int(user_id))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
