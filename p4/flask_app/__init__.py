# flask_app/__init__.py
from flask import Flask, render_template
from werkzeug.utils import secure_filename
import os

from .client import PostClient
from .extensions import db, login_manager, bcrypt  # ✅ now import from extensions

OMDB_API_KEY = '739f26fa'
if os.getenv('OMDB_API_KEY'):
    OMDB_API_KEY = os.getenv('OMDB_API_KEY')

Post_client = PostClient()

def custom_404(e):
    return render_template("404.html"), 404

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile("config.py", silent=False)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from .users.routes import users
    from .posts.routes import posts 
    app.register_blueprint(users)
    app.register_blueprint(posts)   # ✅ register it


    app.register_error_handler(404, custom_404)
    login_manager.login_view = "users.login"

    return app
