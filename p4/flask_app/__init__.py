# flask_app/__init__.py
<<<<<<< HEAD

from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
post_client = None  # We'll initialize this in create_app
=======
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
>>>>>>> a0997d9a870d24891f1182c64ee02a777f4e41e9

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile("config.py", silent=False)
<<<<<<< HEAD
    
=======
>>>>>>> a0997d9a870d24891f1182c64ee02a777f4e41e9
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

<<<<<<< HEAD
    # Initialize post client
    from .client import PostClient
    global post_client
    post_client = PostClient()

    from .users.routes import users
    from .posts.routes import posts  # Make sure this is "posts" not "movies"

    app.register_blueprint(users)
    app.register_blueprint(posts)  # Make sure this matches the blueprint name

    # Configure login manager
=======
    from .users.routes import users
    from .posts.routes import posts 
    app.register_blueprint(users)
    app.register_blueprint(posts)   # ✅ register it


    app.register_error_handler(404, custom_404)
>>>>>>> a0997d9a870d24891f1182c64ee02a777f4e41e9
    login_manager.login_view = "users.login"
    
    # Error handler
    app.register_error_handler(404, lambda e: (render_template("404.html"), 404))

    return app
