import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, CommentForm
from flask import Flask, render_template, request, flash, url_for, redirect
from config import Config

blog = Flask(__name__)
blog.config.from_object(Config)
db = SQLAlchemy(blog)

from models import *


# template for converting Month to number
@blog.template_filter("format_datetime")
def format_datetime(dto):
    return dto.strftime('%B %d, %Y')


# sidebar data loader
def sidebar_data():
    recent = Post.query.order_by(Post.posted_on.desc()).limit(5).all()
    tags = Tag.query.all()

    return recent, tags


# route for the index page
@blog.route('/')
@blog.route('/posts')
def index():
    page = request.args.get('page', 1, type=int)
    data = Post.query.order_by(Post.posted_on.desc()).paginate(page=page, per_page=6)
    recent , tags = sidebar_data()
    return render_template('index.html', title="Welcome to askAma", data=data, posts=recent, sidedata=tags)


# route for individual posts
@blog.route('/posts/<int:year>/<int:month>/<string:slug>', methods=['GET', 'POST'])
def post(year, month, slug):
    form = CommentForm()
    if form.validate_on_submit():
        print(form.username.data, form.comment.data)
    data = Post.query.first_or_404(slug)
    return render_template('post.html', info=data, form=form)


# route for tags
@blog.route('/category/<tag>')
def category(tag):
    # page = request.args.get('page', 1, type=int)
    data = Tag.query.first_or_404(tag).posts
    recent, tags = sidebar_data()
    return render_template('tag.html', title=f'Tag - {tag}', data=data, posts=recent, sidedata=tags)


# route for authors
@blog.route('/author/<username>')
def author(username):
    data = User.query.filter_by(username=username).first().post
    recent , tags = sidebar_data()
    return render_template('author.html', title=f'Author - {username}', data=data, sidedata=tags, posts=recent)


# login route
@blog.route('/login', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data, form.password.data)
    return render_template("signin.html", title="Signin to askAma", form=form)


# signup route
@blog.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # account = User(username=form.username.data, email=form.email.data, password=form.password.data)
        # db.session.add(account)
        # db.session.commit()
        flash(f'flash account created for {form.username.data}', 'success')
        return redirect(url_for('index'))
    return render_template("signup.html", title="Join askAma", form=form)


if __name__ == "__main__":
    host = os.environ.get('IP', '127.0.1.1')
    port = int(os.environ.get('PORT', 8080))
    blog.run(host=host, port=port, debug=True, use_reloader=True)
