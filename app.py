import os

import dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

dotenv.load_dotenv()
app = Flask(__name__)


db_user = os.getenv("DB_USER")
if db_user is None:
    raise ValueError("DB_USER must not be None")
db_pass = os.getenv("DB_PASS")
if db_pass is None:
    raise ValueError("DB_PASS must not be None")
db_host = os.getenv("DB_HOST")
if db_host is None:
    db_host = "localhost"
db_port = os.getenv("DB_PORT")
if db_port is not None:
    db_host = f"{db_host}:{db_port}"
db_name = os.getenv("DB_NAME")
if db_name is None:
    db_name = "backend"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
app.config['JSON_AS_ASCII'] = False
app.config["JWT_SECRET_KEY"] = os.getenv("LOGIN_SECRET")

# noinspection PyUnresolvedReferences
import backend.api
# noinspection PyUnresolvedReferences
import backend.model


jwt = JWTManager(app)
db: SQLAlchemy = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()
