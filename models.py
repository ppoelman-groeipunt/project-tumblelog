from mongoengine import *
from datetime import datetime, UTC
from flask_login import UserMixin


class User(Document, UserMixin):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    alias = StringField(max_length=20, required=True)

    # `UserMixin` provides the required attributes and methods:
    # is_authenticated
    # is_active
    # is_anonymous
    # get_id()


class Comment(EmbeddedDocument):
    content = StringField(required=True)
    author = ReferenceField('User', required=True)
    timestamp = DateTimeField(default=datetime.now(UTC))


class Post(Document):
    title = StringField(max_length=100, required=True)
    author = ReferenceField('User', reverse_delete_rule=CASCADE, required=True)
    tags = ListField(StringField(max_length=30))
    timestamp = DateTimeField(default=datetime.now(UTC))
    comments = ListField(EmbeddedDocumentField(Comment))
    meta = {'allow_inheritance': True}


class TextPost(Post):
    content = StringField()


class ImagePost(Post):
    image_path = StringField()


class LinkPost(Post):
    link_url = StringField()
