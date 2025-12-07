"""
Comment service layer - handles all comment-related business logic
"""
from datetime import datetime
from personalblog.models import Comment
from personalblog import db


class CommentService:
    @staticmethod
    def create_comment(content, owner, post):
        """Create a new comment"""
        comment = Comment(content=content, owner=owner, post=post)
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def get_comments_by_post(post_id):
        """Get all comments for a specific post"""
        return Comment.query.filter_by(post_id=post_id).order_by(Comment.date_posted.asc()).all()

    @staticmethod
    def get_comment_by_id(comment_id):
        """Get a comment by ID"""
        return Comment.query.get(comment_id)

    @staticmethod
    def update_comment(comment, content):
        """Update a comment"""
        comment.content = content
        comment.posted_on = datetime.utcnow()
        db.session.commit()
        return comment

    @staticmethod
    def delete_comment(comment):
        """Delete a comment"""
        db.session.delete(comment)
        db.session.commit()