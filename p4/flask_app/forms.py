from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

from .models import User

# Search a post
class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


class PostForm(FlaskForm):
    content = StringField("Title", validators=[InputRequired(), Length(min=5, max=500)])
    category = SelectField(
        "Category",
        choices=[("sports", "Sports"), ("news", "News"), ("entertainment", "Entertainment")],
        validators=[InputRequired()]
    )
    image = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Create Post")


# Comment on a post
class CommentForm(FlaskForm):
    content = StringField("Add a Comment", validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField("Post Comment")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

class UpdateUsernameForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    submit_username = SubmitField("Update Username") 

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None and user.username != current_user.username:
            raise ValidationError("Username is taken")

class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Photo', validators=[
        FileRequired(), 
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images Only!')
    ])
    submit_picture = SubmitField('Update Picture')
