from sqlalchemy.orm import DeclarativeBase
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
  pass

# create the app
app = Flask(__name__)
db = SQLAlchemy(model_class=Base)



