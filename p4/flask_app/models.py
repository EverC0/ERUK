from flask_login import UserMixin
from datetime import datetime
# from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from .extensions import db, login_manager
from mongoengine import StringField, ReferenceField, EmailField, ImageField
# from mongoengine import FileField as MongoFileField

# TODO: implement
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

# TODO: implement fields
class User(db.Document, UserMixin):
    username = StringField(required=True, unique=True, min_length=1, max_length=40)
    email = EmailField(required=True, unique=True)
    password =  StringField(required=True)
    profile_pic = ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


# TODO: implement fields
# instead of reviews will change this to user posts

# Rename Review -> Post
class Post(db.Document):
    author = ReferenceField(User, required=True)
    content = StringField(required=True, min_length=5, max_length=500)
    category = StringField(required=True, choices=["sports", "news", "entertainment"])  # New field
    image = ImageField()  # Replace movie poster with user-uploaded image
    date = StringField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))