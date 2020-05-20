from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_cors import CORS


pymysql.install_as_MySQLdb()
app = Flask('wbserver')
app.config.from_pyfile('app/settings.py')
db = SQLAlchemy(app)
CORS(app)
from . import views,models