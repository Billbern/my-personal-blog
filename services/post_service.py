"""
Post service layer - handles all post-related business logic
"""
from datetime import datetime
from personalblog.models import Post, Comment
from personalblog import db


class PostService:
    @staticmethod
    def get_all_posts():
        """Get all posts ordered by date posted"""
        return Post.query.order_by(Post.posted_on.desc()).all()

    @staticmethod
    def get_post_by_id(post_id):
        """Get a post by ID"""
        return Post.query.get(post_id)

    @staticmethod
    def create_post(title, content, user_id):
        """Create a new post"""
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def update_post(post, title, content):
        """Update a post"""
        post.title = title
        post.content = content
        post.posted_on = datetime.utcnow()
        db.session.commit()
        return post

    @staticmethod
    def delete_post(post):
        """Delete a post and its comments"""
        # Delete all comments associated with the post first
        Comment.query.filter_by(post_id=post.id).delete()
        db.session.delete(post)
        db.session.commit()

    @staticmethod
    def search_posts(query_string):
        """Search posts by title or content"""
        search = f"%{query_string}%"
        return Post.query.filter(
            Post.title.like(search) | Post.content.like(search)
        ).order_by(Post.posted_on.desc()).all()