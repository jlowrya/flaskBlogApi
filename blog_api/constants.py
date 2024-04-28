from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


class Base(DeclarativeBase):
  pass

# create the app
app = Flask(__name__)
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/blogs.db"


# initialize the app with the extension
db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)


app.secret_key = "145e19eb2f010f39e1f55c89eaf301355fab2f343442f17ad93e3d5d33a076a0"
