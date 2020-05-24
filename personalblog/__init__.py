from flask import Flask
from personalblog.config import Config
from flask_sqlalchemy import SQLAlchemy


blog = Flask(__name__)
blog.config.from_object(Config)
db = SQLAlchemy(blog)


from personalblog import routes