# flask_app/__init__.py

from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
post_client = None  # We'll initialize this in create_app

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile("config.py", silent=False)
    
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Initialize post client
    from .client import PostClient
    global post_client
    post_client = PostClient()

    from flask_dance.consumer import OAuth2ConsumerBlueprint
    google_blueprint = OAuth2ConsumerBlueprint(
        "google",
        __name__,
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        scope=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ],
        base_url="https://www.googleapis.com/",
        authorization_url="https://accounts.google.com/o/oauth2/auth",
        token_url="https://accounts.google.com/o/oauth2/token",
        redirect_to="users.google_login",
    )
    

    from .users.routes import users
    from .posts.routes import posts 

    app.register_blueprint(users)
    app.register_blueprint(posts)  

    app.register_blueprint(google_blueprint, url_prefix="/login")

    # Configure login manager
    login_manager.login_view = "users.login"
    
    # Error handler
    app.register_error_handler(404, lambda e: (render_template("404.html"), 404))

    return app
