import os
import json
from flask import Flask, render_template, redirect, url_for, request


blog = Flask(__name__)

# route for the index page
@blog.route('/')
@blog.route('/posts')
def index():

    # dict for changing month to number
    mnt = { "January": 1, "February": 2, "March": 3, "April": 4, "May" : 5, 
            "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, 
             "November": 11, "December": 12
        }

    # call the load_data function
    data = load_data()
    return render_template('index.html', title="Welcome to askAma", data=data, mnt=mnt)

# route for individual posts
@blog.route('/posts/<int:year>/<int:month>/<post_title>', methods=['GET', 'POST'])
def post(year, month, post_title):
    
    # call load_data for only posts
    data = load_data()["posts"]
    for item in data:
        if item['postTitle'].lower().replace(' ', '-') == post_title:
            return render_template('post.html', info=item, title=item['postTitle'])

# login route
@blog.route('/login', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html", title="Signin to askAma")

# signup route
@blog.route('/signup')
def signup():
    return render_template("signup.html", title="Join askAma")

# function to load data from json file
def load_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    host = os.environ.get('IP', '127.0.1.1')
    port = int(os.environ.get('PORT', 8080))
    blog.run(host=host, port=port, debug=True, use_reloader=True)
