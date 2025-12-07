from datetime import datetime
from personalblog.models import *
from flask import render_template, request, flash, url_for, redirect
from personalblog.forms import RegistrationForm, LoginForm, CommentForm
from flask_login import login_user, current_user, logout_user, login_required


from personalblog import blog, db


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
    data = Post.query.filter_by(slug=slug).first_or_404()
    if form.validate_on_submit():
        comment = Comment(owner=form.username.data, content=form.comment.data, post=data)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('post', year=year, month=month, slug=slug))
    return render_template('post.html', info=data, form=form)


# route for tags
@blog.route('/category/<tag>')
def category(tag):
    data = Tag.query.filter_by(name=tag).first_or_404().posts
    recent, tags = sidebar_data()
    return render_template('tag.html', title=f'Tag - {tag}', data=data, 
                                        posts=recent, sidedata=tags,
                                        caption=f'Posts under {tag}')


# route for authors
@blog.route('/author/<username>')
def author(username):
    data = User.query.filter_by(username=username).first_or_404().posts
    recent, tags = sidebar_data()
    return render_template('author.html', title=f'Author - {username}', 
                                        data=data, sidedata=tags, 
                                        posts=recent, caption=f'Posts by {username}')


# login route
@blog.route('/login', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Check email or password', 'danger')
    return render_template("signin.html", title="Signin to askAma", form=form)

# logout route
@blog.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

# signup route
@blog.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        account = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(account)
        db.session.commit()
        flash(f'Account created for {form.username.data}, you are now logged in', 'success')
        login_user(account)
        return redirect(url_for('index'))
    return render_template("signup.html", title="Join askAma", form=form)

@blog.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')
