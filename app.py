import os
from time import strptime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request


blog = Flask(__name__)
blog.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
blog.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(blog)

from models import *


# template for converting route string
@blog.template_filter("convert_string")
def convert_string(string):
    return string.lower().replace(' ', '-')


# template for converting Month to number
@blog.template_filter("format_datetime")
def format_datetime(dto):
    return strptime(dto, '%B').tm_mon


#sidebar data loader
def sidebar_data():
    recent = Post.query.order_by(Post.posted_on.desc()).limit(5).all()
    tags = Tag.query.all()

    return recent, tags


# route for the index page
@blog.route('/')
@blog.route('/posts')
def index():
    page = request.args.get('page', 1, type=int)
    data = Post.query.paginate(page=page, per_page=10)
    recent , tags = sidebar_data()
    return render_template('index.html', title="Welcome to askAma", data=data.items, posts=recent, sidedata=tags)


# route for individual posts
@blog.route('/posts/<int:year>/<int:month>/<string:post_title>', methods=['GET', 'POST'])
def post(year, month, post_title):
    return render_template('post.html')


# route for tags
@blog.route('/category/<tag>')
def category(tag):
    data = Tag.query.filter_by(name=tag).all()[0].posts
    recent , tags = sidebar_data()
    return render_template('tag.html', title=f'Tag - {tag}', data=data, posts=recent, sidedata=tags)


# route for authors
@blog.route('/author/<username>')
def author(username):
    data = User.query.filter_by(username=username).all()[0].post
    recent , tags = sidebar_data()
    return render_template('author.html', title=f'Author - {username}', data=data, sidedata=tags, posts=recent)


# login route
@blog.route('/login', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html", title="Signin to askAma")


# signup route
@blog.route('/signup')
def signup():
    return render_template("signup.html", title="Join askAma")


if __name__ == "__main__":
    host = os.environ.get('IP', '127.0.1.1')
    port = int(os.environ.get('PORT', 8080))
    blog.run(host=host, port=port, debug=True, use_reloader=True)
