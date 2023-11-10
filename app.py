import os

import dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


def getenv_or_default(key: str, default: str) -> str:
    result = os.getenv(key)
    if result is None:
        return default
    return result


dotenv.load_dotenv()
app = Flask(__name__)

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/sales-mail-assist'
app.config['JSON_AS_ASCII'] = False
app.config["JWT_SECRET_KEY"] = os.getenv("LOGIN_SECRET")

jwt = JWTManager(app)
db: SQLAlchemy = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()
