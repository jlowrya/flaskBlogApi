from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
  pass

# create the app
app = Flask(__name__)
db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/blogs.db"


# initialize the app with the extension
db.init_app(app)
migrate = Migrate(app, db)



