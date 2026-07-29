from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail(app)

from flaskstart.admin_panel.routes import adminpanel
from flaskstart.errors.handlers import errors
from flaskstart.main.routes import main
from flaskstart.posts.routes import posts
from flaskstart.support.routes import support_page
from flaskstart.users.routes import users

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)
app.register_blueprint(support_page)
app.register_blueprint(adminpanel)

with app.app_context():
    db.create_all()
