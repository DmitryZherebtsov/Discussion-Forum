from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskstart.forms import RegitrationForm, LoginForm

app = Flask(__name__) # екземпляр застосунку під назвою app
app.config['SECRET_KEY'] = 'ce9b10bbc3ba4db3e0b1b5274d1a0517'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from flaskstart import routes