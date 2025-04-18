import io
from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """
# login and register do nothing here for right now

# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("ok.index"))
    
    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        username = registration_form.username.data
        email = registration_form.email.data
        password = registration_form.password.data

        hashed_password = bcrypt.generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password, profile_pic=None)
        user.save()
        flash("Account created successfully!", "success")
        return redirect(url_for("users.login"))
    
    error_msg = None
    if request.method == "POST" and not registration_form.validate():
        error_msg = "Registration was not successful"

    return render_template("register.html", form=registration_form, error_msg=error_msg)


# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("ok.index")) 
    
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        user = User.objects(username=login_form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')

    return render_template("login.html", form=login_form)

# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("ok.index"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():

    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
   
    # TODO: handle update username form submit
    if update_username_form.submit_username.data and update_username_form.validate(): 
        
        new_username = update_username_form.username.data
        current_user.modify(username=new_username)
        current_user.save()
        flash("Username updated successfully!", "success")
        return redirect(url_for("users.account"))   
        
    
    # TODO: handle update profile pic form submit
    if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
        img = update_profile_pic_form.picture.data
        filename = secure_filename(img.filename)
        content_type = img.content_type  # safer than inferring from extension

        if current_user.profile_pic.get() is None:
            current_user.profile_pic.put(img.stream, content_type=content_type, filename=filename)
        else:
            current_user.profile_pic.replace(img.stream, content_type=content_type, filename=filename)

        current_user.save()
        flash("Image updated successfully!", "success")
        return redirect(url_for("users.account"))   

        
    image = None
    if current_user.profile_pic:
        try:
            bytes_io = io.BytesIO(current_user.profile_pic.read())
            image = base64.b64encode(bytes_io.getvalue()).decode()
        except Exception as e:
            print(f"Error reading profile_pic: {e}")
            pass

    return render_template(
        "account.html",
        update_username_form=update_username_form,
        update_profile_pic_form=update_profile_pic_form,
        image=image,
        error="update account was not successful"
    )

