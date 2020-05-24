from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from personalblog.config import Config
from flask_sqlalchemy import SQLAlchemy


blog = Flask(__name__)
blog.config.from_object(Config)

db = SQLAlchemy(blog)
migrate = Migrate(blog, db)

loginmanager = LoginManager(blog)
loginmanager.login_view = 'signin'
loginmanager.login_message_category = 'info'


from personalblog import routes