import os
import json
from time import strptime
from flask_paginate import Pagination, get_page_args
from flask import Flask, render_template, redirect, url_for, request


blog = Flask(__name__)

# template for converting route string
@blog.template_filter("convert_string")
def convert_string(string):
    return string.lower().replace(' ', '-')

# template for converting Month to number
@blog.template_filter("format_datetime")
def format_datetime(dto):
    return strptime(dto, '%B').tm_mon

# load data from json file
def load_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data

# load requested paginated data
def get_posts(data, offset=0, per_page=10):
    return data[offset: offset + per_page]


# route for the index page
@blog.route('/')
@blog.route('/posts')
def index():
    # call the load_data function
    data = load_data()["posts"]
    
    # get and set page parameters for pagination
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users = get_posts(data, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=len(data), css_framework='bootstrap4')
    # return render_template('index.html', users=pagination_users, page=page, per_page=per_page, pagination=pagination )
    
    return render_template('index.html', title="Welcome to askAma", data=pagination_users,
                                                                    pagination= pagination,
                                                                    posts=data)

# route for individual posts
@blog.route('/posts/<int:year>/<int:month>/<string:post_title>', methods=['GET', 'POST'])
def post(year, month, post_title):
    
    # call load_data for only posts
    data = load_data()["posts"]
    
    # check if requested page exists then render it
    for item in data:
        if item['postTitle'].lower().replace(' ', '-') == post_title:
            return render_template('post.html', info=item, title=item['postTitle'])


@blog.route('/category/<tag>')
def category(tag):
    data = load_data()['posts']
    newdata = []
    for post in data:
        if tag in post['tags']:
            newdata.append(post)
    return render_template('tag.html', caption=f'Posts under {tag}', data=newdata, posts=data)

@blog.route('/author/<username>')
def author(username):
    data =load_data()['posts']
    newdata = []
    for post in data:
        if username == post['author']:
            newdata.append(post)
    return render_template('author.html', caption=f'Posts by {username}', data=newdata, posts=data)

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
