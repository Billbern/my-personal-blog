"""
User service layer - handles all user-related business logic
"""
from werkzeug.security import generate_password_hash
from personalblog.models import User
from personalblog import db


class UserService:
    @staticmethod
    def create_user(username, email, password):
        """Create a new user with hashed password"""
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return User.query.filter_by(email=email).first()



    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user by email and password"""
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            return user
        return None