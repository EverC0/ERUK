from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
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

class Review(db.Document):
    commenter = ReferenceField(User, required=True)
    content = StringField(required=True, min_length=5, max_length=500)
    date = StringField(required=True, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    imdb_id = StringField(required=True, min_length=9, max_length=9)
    movie_title = StringField(required=True, min_length=1, max_length=100)
    # image = db.StringField()
    #Uncomment when other fields are ready for review pictures