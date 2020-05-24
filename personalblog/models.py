from datetime import datetime
from flask_login import UserMixin
from personalblog import db, loginmanager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash


@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    pic = db.Column(db.String, nullable=False, default='/static/img/author_default.png')
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    post = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.pic}')"
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    slug = db.Column(db.String(140), nullable=False)
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    featured_img = db.Column(db.String, nullable=False, default='/static/img/default-img.png')
    summary = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=False)
    comment = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship('Tag', secondary='tagging')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    _non_safe = ['"', '\'', '#', '$', '%', '&', '+', ',', '/', ':', ';', '=',
                    '?', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~']
    _translate_table = {ord(char): u'' for char in _non_safe}

    @staticmethod
    def _slugify(state, value, previous, initiator):
        text = value.translate(_translate_table)
        state.slug = u'-'.join(text.lower().split())

    def __repr__(self):
        return f"Post('{self.title}', '{self.posted_on}')"


db.event.listen(Post.title, 'set', Post._slugify, retval=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(20), unique=True, nullable=False)
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.owner}', '{self.content}', '{self.posted_on}')"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', secondary='tagging')

    def __repr__(self):
        return f"Tag('{self.name}')"


class Tagging(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    post = db.relationship('Post', backref=db.backref('tagging', cascade="all, delete-orphan"))
    tag = db.relationship('Tag', backref=db.backref('tagging', cascade="all, delete-orphan"))
