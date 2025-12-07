"""
Tag service layer - handles all tag-related business logic
"""
from personalblog.models import Tag, Post
from personalblog import db


class TagService:
    @staticmethod
    def get_tag_by_name(tag_name):
        """Get a tag by name"""
        return Tag.query.filter_by(name=tag_name).first()

    @staticmethod
    def get_all_tags():
        """Get all tags"""
        return Tag.query.all()

    @staticmethod
    def get_posts_by_tag(tag_name):
        """Get all posts associated with a specific tag"""
        tag = Tag.query.filter_by(name=tag_name).first_or_404()
        return tag.posts