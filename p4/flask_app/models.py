from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from mongoengine import StringField, ReferenceField, EmailField, ImageField, ListField

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    meta = {
        'indexes': [
            {
                'fields': ['google_id'],
                'unique': True,
                'sparse': True  # Allows multiple nulls
            }
        ]
    }
        
    username = StringField(required=True, unique=True, min_length=1, max_length=40)
    google_id = StringField()
    google_token = StringField()
    email = EmailField(required=True, unique=True)
    password = StringField()
    profile_pic = ImageField()

    def get_id(self):
        return self.username

class Post(db.Document):
    author = ReferenceField(User, required=True)
    content = StringField(required=True, min_length=5, max_length=500)
    category = StringField(required=True, choices=["sports", "news", "entertainment"])
    image = ImageField()
    date = StringField(default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    likes = ListField(ReferenceField(User), default=[])

class Comment(db.Document):
    post = ReferenceField(Post, required=True)
    commenter = ReferenceField(User, required=True)
    content = StringField(required=True, min_length=1, max_length=500)
    date = StringField(default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
