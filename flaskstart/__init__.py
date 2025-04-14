from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flaskstart.forms import RegitrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) # екземпляр застосунку під назвою app
app.config['SECRET_KEY'] = 'ce9b10bbc3ba4db3e0b1b5274d1a0517'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flaskstart import routes