
from flask_migrate import Migrate
from blog_api.models import *
from blog_api.constants import app, db

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/blogs.db"


# initialize the app with the extension
db.init_app(app)
migrate = Migrate(app, db)
