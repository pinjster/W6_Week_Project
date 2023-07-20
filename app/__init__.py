from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from app.blueprints.social import bp as social
app.register_blueprint(social)
from app.blueprints.auth import bp as auth
app.register_blueprint(auth)
from app.blueprints.main import bp as main
app.register_blueprint(main)


from app import models